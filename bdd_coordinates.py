import lxml.etree as LET
import os
from datetime import datetime
import re
import xslt_styles
import roman
import argparse
import config
import json


page_xml_ns = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"
tei_ns = "http://www.tei-c.org/ns/1.0"
xml_ns = "http://www.w3.org/XML/1998/namespace"


def load_tei_file(path_tei):
    tree = LET.parse(path_tei)
    root = tree.getroot()

    return root


def delete_wrong_atributes(root, attribute):
    for element in root.iter():
        if attribute in element.attrib:
            del element.attrib[attribute]

    return root


def coords_baseline(root, id, sigle):
    # get line with id
    line = root.findall(
        ".//{" + page_xml_ns + "}TextLine[@id='" + str(id) + "']")[0]
    # scaling factor for coordinates
    # iiif_scale_factor F 1.34
    x = config.manuscript_data[sigle]["iiif_scale_factor"]

    # fetch coordinates using XPath query from the PAGE XML document root
    coords = line.xpath('.//ns0:Baseline/@points',
                        namespaces={'ns0': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'})
    # iterate over all coordinate sets found
    for i in coords:
        # split the coordinates by space (expected format is "x1,y1 x2,y2 ... xn,yn")
        coord = i.split(' ')
        # split the leftmost (first) coordinate by comma into x and y values
        coord_left = coord[0].split(',')
        # split the rightmost (last) coordinate by comma into x and y values
        coord_right = coord[-1].split(',')
        # calculate adjusted x-coordinate (c1) and y-coordinate (c2) of the leftmost point of the baseline
        # scale the original x-coordinate by the factor x and reduce by 20
        c1 = int(int(coord_left[0]) * x) - 50
        # scale the original y-coordinate by the factor x and reduce by 50
        c2 = int(int(coord_left[1]) * x) - 50
        # calculate the width of the baseline (the x-distance between the leftmost and rightmost points)
        w = int(coord_right[0]) - int(coord_left[0]) + \
            80  # add 80 to the width
        # scale the width by the factor x
        w = int(w * x)
        # fix the height of the baseline at 100
        h = 150
    # format the calculated values into a string "c1,c2,w,h"
    coord_string = f"{c1},{c2},{w},{h}"
    return coord_string


def add_coordinates_to_missing_facs(root, tei_root, sigle):
    # get all lines in tei
    lines = tei_root.findall(".//{" + tei_ns + "}lb")
    #print(lines)
    for line in lines:
        try:
            if line.get("facs") == None:
                # get line id
                line_id = line.get("{" + xml_ns + "}id")
                line.set("facs", coords_baseline(root, line_id, sigle))
                print(LET.tostring(line))

                print(str(line_id))
        except Exception as e:
            #print(LET.tostring(line))

            print(e, str(line_id))


def copy_id_to_expan(line):
    # print(LET.tostring(line))
    if line != None and line.getparent().tag == "{http://www.tei-c.org/ns/1.0}abbr":
        # get lb in expan
        lb = line.getparent().getparent().find(
            ".//{http://www.tei-c.org/ns/1.0}expan//{http://www.tei-c.org/ns/1.0}lb")
        #print(LET.tostring(line))

        #print(line.getparent().tag)
        print(LET.tostring(line))
        print(LET.tostring(lb))
        print("___________________")
        # get id of line
        id = line.get("{" + xml_ns + "}id")
        id = id + "_expan"
        # set id of lb
        lb.set("{" + xml_ns + "}id", id)


def add_chapter_number_to_num(xml):
    num_elements = xml.findall(".//{" + tei_ns + "}num")
    for element in num_elements:
        # set type of num to 'chapter-number'
        element.set("type", "chapter-number")

def set_id_of_tei_elements(root, index, file_name, number_of_files, remaining_pbs, page_xml_root):
    if index <= number_of_files:
        # get current pb element based on index number
        pb = root.findall(".//{" + tei_ns + "}pb")[index]
        pb.set("{" + xml_ns + "}id", file_name)
        # get current fw element based on index number
        fw = root.findall(".//{" + tei_ns + "}fw[@type='page-header']")[index]
        fw.set("{" + xml_ns + "}id", file_name + "_header")
        # get current cba element based on index number
        cba = root.findall(".//{" + tei_ns + "}cb[@n='a']")[index]
        cba.set("{" + xml_ns + "}id", file_name + "_column_1")
        # get current cbb element based on index number
        cbb = root.findall(".//{" + tei_ns + "}cb[@n='b']")[index]
        cbb.set("{" + xml_ns + "}id", file_name + "_column_2")
        # get each <lb/> element between current cba and cbb
        lbs = root.xpath(f'.//tei:lb[preceding::tei:pb[not(ancestor::tei:expan)][{index + 1}] and count(preceding::tei:cb[@n="b"][not(ancestor::tei:expan)]) = {index + 1} and not(ancestor::tei:expan) and not(ancestor::tei:note[@type="inscription"])]', namespaces={
                         'tei': 'http://www.tei-c.org/ns/1.0'})
        i = 1
        for l in lbs:
            l.set("{" + xml_ns + "}id", file_name +
                  "_column_2_l_" + str(i).zfill(2))
            copy_id_to_expan(l)
            i += 1
        # get each <lb/> element between current cbb and next pb
        lbs = root.xpath(f'.//tei:lb[count(preceding::tei:cb[@n="b"][not(ancestor::tei:expan)]) = {index} and count(preceding::tei:cb[@n="a"][not(ancestor::tei:expan)]) = {index + 1} and not(ancestor::tei:expan) and not(ancestor::tei:note[@type="inscription"])]', namespaces={
                         'tei': 'http://www.tei-c.org/ns/1.0'})
        i = 1
        for l in lbs:
            l.set("{" + xml_ns + "}id", file_name +
                  "_column_1_l_" + str(i).zfill(2))
            copy_id_to_expan(l)
            i += 1
        # get all chapter count elements between current <pb> and next
        chapter_counts = root.xpath(
            f".//tei:label[count(preceding::tei:pb[not(ancestor::tei:expan)]) = {index + 1} and count(following::tei:pb[not(ancestor::tei:expan)]) = {remaining_pbs-1}]", namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
        # sort remaining_pbs based on n attribute
        
        chapter_counts = sorted(chapter_counts, key=lambda x: int(x.get("n")))
        n = 1
        for chapter_count in chapter_counts:
            chapter_count.set("{" + xml_ns + "}id", file_name +
                              "_chapter_count_" + str(n).zfill(3))
            change_id_of_chapter_count(page_xml_root, chapter_count)
            n += 1

            
        # get all inscription elements between current <pb> and next
        inscriptions = root.xpath(
            f".//tei:note[@type='inscription'][count(preceding::tei:pb[not(ancestor::tei:expan)]) = {index + 1} and count(following::tei:pb[not(ancestor::tei:expan)]) = {remaining_pbs-1}]", namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
        n = 1
        for inscription in inscriptions:
            inscription.set("{" + xml_ns + "}id", file_name +
                            "_inscription_" + str(n).zfill(2))
            print(LET.tostring(inscription))

            # change attribute of num
            add_chapter_number_to_num(inscription)

            change_id_of_inscription(page_xml_root, inscription)

            # get all <lb> elements in inscription
            lbs = inscription.findall(".//{" + tei_ns + "}lb")
            # add n element and xml:id to each <lb> element
            i = 1
            for l in lbs:
                l.set("{" + xml_ns + "}id", file_name + "_inscription_" +
                      str(n).zfill(2) + "_l_" + str(i).zfill(2))
                l.set("n", str(i))
                copy_id_to_expan(l)
                i += 1
            n += 1

    return root


def let_findall(root, xpath, start_element, end_element):
    elements = []
    found_start = False
    for element in root.iter():
        if element == start_element:
            found_start = True
        elif element == end_element:
            break
        if found_start and element.tag == xpath:
            elements.append(element)

    return elements


def load_pagexml_file(path):
    tree = LET.parse(path)
    root = tree.getroot()

    return root


def set_metadata(root):
    # Set Creator
    creator = root.find(".//{" + page_xml_ns + "}Creator")
    creator.text = "PageXML created by Burchards Dekret Digital."
    # Set timestamp
    timestamp = root.find(".//{" + page_xml_ns + "}Created")
    timestamp.text = str(datetime.now())
    # Remove Transkribus metadata
    metadata = root.find(".//{" + page_xml_ns + "}Metadata")
    transkribus_metadata = root.find(
        ".//{" + page_xml_ns + "}TranskribusMetadata")
    metadata.remove(transkribus_metadata)

    return root


def create_link_to_image(root, iiif_start_number, sigle):
    page = root.find(".//{" + page_xml_ns + "}Page")
    width = page.get("imageWidth")
    height = page.get("imageHeight")
    image_name = page.get("imageFilename")

    link_to_image = config.manuscript_data[sigle]["facs_url"]
    link_to_image = link_to_image.replace("{iiif_start_number}", str(iiif_start_number))
    link_to_image = link_to_image.replace("{width}", str(width))
    link_to_image = link_to_image.replace("{height}", str(height))

    return {"file_name": image_name.replace("jpg","xml"), "image_name": image_name, "url": link_to_image}

def save_json(images_list, sigle, book_number, expan):
    if expan:
        path = os.path.join(os.getcwd(), "pagexml", sigle,
                                book_number, "expan", "images.json")
    else:
        path = os.path.join(os.getcwd(), "pagexml", sigle,
                                book_number, "abbr", "images.json")
    with open(path, "w+") as json_file:
        json.dump(images_list, json_file, indent=4)


def remove_page_elements(root):
    page = root.find(".//{" + page_xml_ns + "}Page")
    reading_order = root.find(".//{" + page_xml_ns + "}ReadingOrder")
    page.remove(reading_order)

    return root


def remove_text_equiv(root):
    text_regions = root.findall(".//{" + page_xml_ns + "}TextRegion")
    for text_region in text_regions:
        text_equiv = text_region.find("./{" + page_xml_ns + "}TextEquiv")
        text_region.remove(text_equiv)

    return root


def change_id_of_inscription(root, inscription):
    # get n value of inscription based on parent
    n_value = inscription.getparent().get("n")
    # get xml:id of inscription
    xml_id = inscription.get("{" + xml_ns + "}id")
    inscriptions_pagexml = root.xpath(f".//page:TextRegion[contains(@custom, 'Inskription')]", namespaces={
                                      'page': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'})
    for inscription_pagexml in inscriptions_pagexml:
        if inscription_pagexml.findall(".//{" + page_xml_ns + "}TextLine/{" + page_xml_ns + "}TextEquiv/{" + page_xml_ns + "}Unicode")[0].text.startswith(f"*{n_value}*"):
            inscription_pagexml.set("id", xml_id)


def change_id_of_chapter_count(root, chapter_count):
    # get n value of chapter_count
    n_value = chapter_count.get("n")
    xml_id = chapter_count.get("{" + xml_ns + "}id")
    # get name of parent of chapter_count
    parent = chapter_count.getparent().tag
    # get text region starting with ~n~ value or *n* value
    chapter_counts_pagexml = root.xpath(f".//page:TextRegion[contains(@custom, 'chapter_count')]", namespaces={
                                        'page': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'})
    for chapter_count_pagexml in chapter_counts_pagexml:
        if parent == "{http://www.tei-c.org/ns/1.0}item":
            if chapter_count_pagexml.findall(".//{" + page_xml_ns + "}TextLine/{" + page_xml_ns + "}TextEquiv/{" + page_xml_ns + "}Unicode")[0].text.startswith(f"~{n_value}~"):
                chapter_count_pagexml.set("id", xml_id)
        else:
            if chapter_count_pagexml.findall(".//{" + page_xml_ns + "}TextLine/{" + page_xml_ns + "}TextEquiv/{" + page_xml_ns + "}Unicode")[0].text.startswith(f"*{n_value}*"):
                chapter_count_pagexml.set("id", xml_id)


def change_id_of_textregion(root, pageNr):
    text_regions = root.findall(".//{" + page_xml_ns + "}TextRegion")
    for text_region in text_regions:
        # check type
        if "header" in text_region.get("custom"):
            text_region.set("id", pageNr + "_header")
        elif "footer" in text_region.get("custom"):
            text_region.set("id", pageNr + "_footer")
        # elif "Inskription" in text_region.get("custom"):
        #    text_region.set("id", pageNr + "_inscription_" + str(n_ins))
        #    n_ins += 1
        elif "column_1" in text_region.get("custom"):
            text_region.set("id", pageNr + "_column_1")
        elif "column_2" in text_region.get("custom"):
            text_region.set("id", pageNr + "_column_2")

    return root


def create_line_id(root):
    text_regions = root.findall(".//{" + page_xml_ns + "}TextRegion")
    for text_region in text_regions:
        n = 1
        lines = text_region.findall(".//{" + page_xml_ns + "}TextLine")
        for line in lines:
            line.set("id", text_region.get("id") + "_l_" + str(n).zfill(2))
            n += 1

    return root


def replace_text(root, tei_root, list_of_tei_lines, xslt):
    # get all text regions
    text_regions = root.findall(".//{" + page_xml_ns + "}TextRegion")

    # iterate though elements and change text using abbr
    for text_region in text_regions:
        #print(LET.tostring(text_region))
        if "header" in text_region.get("custom"):
            get_and_set_text_of_elements(
                text_region, ".//tei:fw", tei_root, xslt)

        elif "chapter_count" in text_region.get("custom"):
            get_and_set_text_of_elements(
                text_region, ".//tei:label", tei_root, xslt)

        elif "column_1" in text_region.get("custom"):
            # get all text lines
            text_lines = text_region.findall("./{" + page_xml_ns + "}TextLine")
            for line in text_lines:
                text_of_line = get_and_set_text_of_empty_elements(
                    line, tei_root, list_of_tei_lines)

        elif "column_2" in text_region.get("custom"):
            # get all text lines
            text_lines = text_region.findall("./{" + page_xml_ns + "}TextLine")
            for line in text_lines:
                text_of_line = get_and_set_text_of_empty_elements(
                    line, tei_root, list_of_tei_lines)

        elif "Inskription" in text_region.get("custom"):
            # get all text lines
            text_lines = text_region.findall("./{" + page_xml_ns + "}TextLine")
            for line in text_lines:
                text_of_line = get_and_set_text_of_empty_elements(
                    line, tei_root, list_of_tei_lines)

    return root


def get_and_set_text_of_elements(text_region, x_path, tei_root, xslt):
    try:
        # get xml_id
        xml_id = text_region.get("id")
        print(xml_id)
        #print(xml_id)
        # get tei element fw with same xml_id
        element = tei_root.find(f"{x_path}[@xml:id='{xml_id}']", namespaces={
                            'tei': 'http://www.tei-c.org/ns/1.0', 'xml': xml_ns})
        # transform fw to abbr text
        print(LET.tostring(element))
        element_text_abbr = transform_to_groundtruth(element, xslt)
        # set text of header
        text_region.find(".//{" + page_xml_ns + "}TextEquiv/{" +
                     page_xml_ns + "}Unicode").text = element_text_abbr
    except:
        pass

def postprocess_text(text):
    #text = re.sub(r'\n', '', text)
    #text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s', '', text)
    text = re.sub(r'#', '\n', text)
    text = re.sub(r'\+\+ ', ' ', text)
    text = re.sub(r'\+\+([A-Za-z])', ' \g<1>', text)
    text = re.sub(r'',' ', text)
    text = re.sub(r' ','', text)
    text = re.sub(r'\+\+', '', text)
    text = re.sub(r'([A-Za-z])', ' \g<1>', text)
    text = re.sub(r'([A-Za-z])', ' \g<1>', text)
    text = re.sub(r'Cap̅ ', 'Cap̅ ', text)
    text = re.sub(r' cap̅ ', ' cap̅ ', text)
    for i in range(1,300):
        roman_numeral = roman.toRoman(i).lower()
        text = re.sub(f' {roman_numeral}', f'{roman_numeral}', text)    
    
    text = text

    return text

def transform_to_groundtruth(xml, xslt):
    #print(LET.tostring(xml))
    xslt_tree = LET.fromstring(xslt)
    # Create an XSLT transformation
    transform = LET.XSLT(xslt_tree)
    # Apply the transformation
    result_tree = transform(xml)
    # delete new lines and spaces
    text = postprocess_text(str(result_tree))
    
    return text


def transform_to_groundtruth_lines(xml, xslt):
    xslt_tree = LET.fromstring(xslt)
    # Create an XSLT transformation
    transform = LET.XSLT(xslt_tree)
    # Apply the transformation
    result_tree = transform(xml)
    # delete new lines and spaces
    text = postprocess_text(str(result_tree))

    return text


def connect_lines(tei_root, xslt_lines):
    column_lines_xslt_output = transform_to_groundtruth_lines(
        tei_root, xslt_lines)
    # print(column_lines_xslt_output)
    column_lines_list = column_lines_xslt_output.split("\n")
    column_lines_list = [line.split("|") for line in column_lines_list]
    # replace "_expan" with "" using comprehension
    column_lines_list = [[re.sub(r'_expan', '', item)
                          for item in line] for line in column_lines_list]

    #print(column_lines_list)

    return column_lines_list

def clean_punctuation(text):
    # distinctio
    text = text.replace('  ','')
    text = text.replace(' ','')
    text = re.sub('(\w)',' \g<1>', text)
    
    # exclamation mark
    text = text.replace(' ','')
    text = re.sub('(\w)',' \g<1>', text)

    # semicolon
    text = text.replace(' ','')
    text = re.sub('(\w)',' \g<1>', text)

    # seg
    text = text.replace('  ',' ')
    text = text.replace(' ','')
    text = text.replace('',' ')
    text = re.sub('(\w)','\g<1> ', text)

    #print(text)
    return text

def get_and_set_text_of_empty_elements(line, tei_root, list_of_tei_lines):
    line_id = line.get("id")
    for item in list_of_tei_lines:
        if line_id == item[0]:
            text_item = item[1]
            #text_item = clean_punctuation(item[1])
            line.find("./{" + page_xml_ns + "}TextEquiv/{" +
                      page_xml_ns + "}Unicode").text = text_item.strip()

def remove_attributes(tei_root):
    for i in ["full", "part", "instant", "org", "sample"]:
        tei_root = delete_wrong_atributes(tei_root, i)

    return tei_root


def save_xml_file(root, path):
    LET.ElementTree(root).write(path, pretty_print=True,
                                encoding="utf-8", xml_declaration=True)


def create_standoff_annotation(root):
    # check if any Textline has $ in Unicode
    text_lines = root.findall(".//{" + page_xml_ns + "}TextLine")
    for text_line in text_lines:
        text = text_line.find(
            "./{" + page_xml_ns + "}TextEquiv/{" + page_xml_ns + "}Unicode").text
        if text:
            # three cases: 3) only § or ß
            # check how many § are in text
            number_of_unclear_beginning = text.count("§")
            number_of_unclear_end = text.count("ß")

            if number_of_unclear_beginning == number_of_unclear_end:
                n = 0
                for i in range(0, number_of_unclear_beginning):
                    # find first occurence of §
                    start = text.find("§") - n
                    end = text.find("ß") - n
                    length = (end - start) - 1
                    # delete first $
                    text = text.replace("§", "", 1)
                    text = text.replace("ß", "", 1)
                    custom_attribut = text_line.get("custom")
                    custom_attribut = custom_attribut + \
                        " unclear {offset:" + \
                        str(start) + "; length:" + str(length) + ";}"
                    # print(custom_attribut)
                    text_line.set("custom", custom_attribut)
                    text_line.find(
                        "./{" + page_xml_ns + "}TextEquiv/{" + page_xml_ns + "}Unicode").text = text
                    n += 2

    return root

def add_angled_dash(tei_root, root, xpath_condition):
    # get all lbs with break='no' in tei_root
    lbs = tei_root.xpath(f".//tei:lb[@break='no'][not(ancestor::tei:expan)]{xpath_condition}", namespaces={
                         'tei': 'http://www.tei-c.org/ns/1.0'})
    # iterate through lbs
    for lb in lbs:
        print(LET.tostring(lb))    

        # get xml id of lb
        id = lb.get("{" + xml_ns + "}id")
        if id != None:
            print(id)
            # find preceeding lb using xpath on tei_root
            preceeding_lb = tei_root.xpath(
                f"//tei:lb[@xml:id='{id}']/preceding::tei:lb[not(ancestor::tei:expan)]{xpath_condition}[1]", namespaces={'tei': 'http://www.tei-c.org/ns/1.0', 'xml': xml_ns})[0]
            # get id of preceeding lb
            id_preceeding = preceeding_lb.get("{" + xml_ns + "}id")
            print(LET.tostring(preceeding_lb))
            print(id_preceeding)
            # check if TextLine with this id is in root
            text_line = root.find(
                ".//{" + page_xml_ns + "}TextLine[@id='"+id_preceeding+"']")
            # if TextLine is in root
            if text_line != None:
                print(LET.tostring(text_line))  

                # appen '¬' to text of TextLine
                text = text_line.find(
                    "./{" + page_xml_ns + "}TextEquiv/{" + page_xml_ns + "}Unicode")
                text.text = text.text + "¬"
            else:
                print("TextLine not found")
    return root







def create_ground_truth(tei_root, root, file, sigle, book_number, expan):
    if expan:
        xslt = xslt_styles.expan_xslt
        xslt_lines = xslt_styles.expan_xslt_for_lines
        xslt_inscription = xslt_styles.expan_xslt_for_lines_inscription
        suffix = "expan_"
    else:
        xslt = xslt_styles.abbr_xslt
        xslt_lines = xslt_styles.abbr_xslt_for_lines
        xslt_inscription = xslt_styles.abbr_xslt_for_lines_inscription
        suffix = "abbr_"

    list_of_tei_lines_inscription = connect_lines(tei_root, xslt_inscription)
    # print(list_of_tei_lines_inscription)
    list_of_tei_lines = connect_lines(tei_root, xslt_lines)
    list_of_tei_lines = list_of_tei_lines + list_of_tei_lines_inscription
    # print(list_of_tei_lines)
    root = replace_text(root, tei_root, list_of_tei_lines, xslt)

    root = create_standoff_annotation(root)

    # for textlines
    root = add_angled_dash(tei_root, root, '[not(ancestor::tei:note)]')
    # for lines in inscription
    root = add_angled_dash(tei_root, root, '[ancestor::tei:note]')


    new_path = os.path.join(os.getcwd(), "pagexml", sigle,
                            book_number, suffix.replace('_', ''), suffix)
    save_xml_file(root, new_path + file)


def iterate_through_pagexml(path, iiif_start_number, number_of_files, remaining_pbs, current_element, tei_root, sigle, book_number):
    images_list = list()
    for file in os.listdir(path):
        if file.endswith(".xml"):
            root = load_pagexml_file(os.path.join(path, file))
            root = set_metadata(root)
            images_list.append(create_link_to_image(root, iiif_start_number, sigle))
            iiif_start_number += 1
            root = remove_page_elements(root)
            root = remove_text_equiv(root)
            root = change_id_of_textregion(root, file[:-4])

            tei_root = set_id_of_tei_elements(
                tei_root, current_element, file[:-4], number_of_files, remaining_pbs, root)
            # needs to come after set_id_of_tei_elements
            root = create_line_id(root)
            current_element += 1
            remaining_pbs -= 1
            add_coordinates_to_missing_facs(root, tei_root, sigle)
            #dash
            create_ground_truth(tei_root, root, file, sigle, book_number, expan=True)
            create_ground_truth(tei_root, root, file, sigle, book_number, expan=False)
    save_json(images_list, sigle, book_number, expan=True)
    save_json(images_list, sigle, book_number, expan=False)

            

    return tei_root


def process_numbers(i, roman_numeral, data):
    data = re.sub(f'<hi rend="color:red"><pc type="distinctio"><g ref="#char-f1f8"></g></pc>{roman_numeral}<pc type="distinctio"><g ref="#char-f1f8"></g></pc></hi>',f'<hi rend="color:red">{roman_numeral}</hi>', data)
    data = re.sub(f'<hi rend="color:red">{roman_numeral}<pc type="distinctio"><g ref="#char-f1f8"></g></pc></hi>',f'<hi rend="color:red">{roman_numeral}</hi>', data)
    data = re.sub(f'<pc type="distinctio"><g ref="#char-f1f8"></g></pc>{roman_numeral}<pc type="distinctio"><g ref="#char-f1f8"></g></pc>', f'<num value="{i}">{roman_numeral}</num>', data)
    data = re.sub(f' {roman_numeral}<pc type="distinctio"><g ref="#char-f1f8"></g></pc>', f' <num value="{i}">{roman_numeral}</num>', data)
    return data

def preprocess_TEI(path_tei, path_temp_tei, list_of_elements_to_be_replaced):
    with open (path_tei, "r", encoding="utf-8") as file:
        data = file.read()
        #g elements that need to be there
        for element in list_of_elements_to_be_replaced:
            data = re.sub(element[0], element[1], data)

        data = re.sub('<choice>\n\s+<abbr>','<choice><abbr>' , data)
        data = re.sub('</abbr>\n\s+<expan>','</abbr><expan>' , data)
        data = re.sub('</expan>\n\s+</choice>','</expan></choice>' , data)

        data = re.sub('<subst>\n\s+<del','<subst><del' , data)
        data = re.sub('"/>\n\s+<add>','"/><add>' , data)
        data = re.sub('</add>\n\s+</subst>','</add></subst>' , data)

        #data = re.sub('(<note type="inscription.*?">)(\w)','\g<1><lb/>\g<2>', data)

        data = re.sub('(<note type="inscription" place="[^"]*" anchored="[^"]*" facs="[^"]*">)(?!<lb)', '\g<1><lb/>', data)


        data = re.sub('\n\s+<label','<label', data)
        data = re.sub('\n\s+<num','<num', data)
        data = re.sub('\n\s+<hi','<hi', data)
        data = re.sub('\n\s+</hi','</hi', data)
        data = re.sub('\n\s+</num','</num', data)
        data = re.sub('\n\s+</hi','</hi', data)
        data = re.sub('\n\s+</label','</label', data)
        data = re.sub('\n\s+</head','</head', data)
        
        # delete <pc> around numbers
        for i in range(1,300):
            roman_numeral = roman.toRoman(i).lower()
            data = process_numbers(i, roman_numeral, data)
            # delete num elements in num elements

        medieval_roman_numbers = [
            [4, 'iiii'],
            [9, 'viiii'],
            [14, 'xiiii'],
            [19, 'xviiii'],
            [24, 'xxiiii'],
            [29, 'xxviiii'],
            [34, 'xxxiiii'],
            [39, 'xxxviiii'],
            [44, 'xxxxiiii'],
            [49, 'xxxxviiii'],
            [54, 'liiii'],
            [59, 'lviiii'],
            [64, 'lxiiii'],
            [69, 'lxviiii'],
            [74, 'lxxiiii'],
            [79, 'lxxviiii'],
            [84, 'lxxxiiii'],
            [89, 'lxxxviiii'],
            [40, 'xxxx'],
            [90, 'lxxxx'],
            [104, 'ciiii'],
            [109, 'cviiii'],
            [114, 'cxiiii'],
            [119, 'cxviiii'],
            [124, 'cxxiiii'],
            [129, 'cxxviiii'],
            [134, 'cxxxiiii'],
            [139, 'cxxxviiii'],
            [144, 'cxxxxiiii'],
            [149, 'cxxxxviiii'],
            [154, 'cliiii'],
            [159, 'clviiii'],
            [164, 'clxiiii'],
            [169, 'clxviiii'],
            [174, 'clxxiiii'],
            [179, 'clxxviiii'],
            [184, 'clxxxiiii'],
            [189, 'clxxxviiii'],
            [190, 'cxxxx'],
            [194, 'cxxxxiiii'],
            [199, 'cxxxxviiii'],
            [204, 'cciiii'],
            [209, 'ccviiii'],
            [214, 'ccxiiii'],
            [219, 'ccxviiii'],
            [224, 'ccxxiiii'],
            [229, 'ccxxviiii'],
            [234, 'ccxxxiiii'],
            [239, 'ccxxxviiii'],
            [244, 'ccxxxxiiii'],
            [249, 'ccxxxxviiii'],
            [254, 'ccliiii'],
            [259, 'cclviiii'],
            [264, 'cclxiiii'],
            [269, 'cclxviiii'],
            [274, 'cclxxiiii'],
            [279, 'cclxxviiii'],
            [284, 'cclxxxiiii'],
            [289, 'cclxxxviiii'],
            [290, 'ccxxxx']
            ]    
        for element in medieval_roman_numbers:
            i = element[0]
            roman_numeral = element[1]
            data = process_numbers(i, roman_numeral, data)

    with open(path_temp_tei, "w", encoding="utf-8") as file:
        file.write(data)

    # replace ecaudata
    pass

def postprocess_TEI(path, list_of_elements_to_be_checked):
    with open (path, "r", encoding="utf-8") as file:
        data = file.read()
        for element in list_of_elements_to_be_checked:
            if element not in data:
                element_text = re.sub('<g .*?>(.*?)</g>','\g<1>',element)
                data = re.sub(element, element_text, data)
    with open(path, "w", encoding="utf-8") as file:
        file.write(data)


def main(sigle, book_number, iiif_start_number):
    iiif_start_number = int(iiif_start_number)
    # variables
    path_tei = os.path.join(os.getcwd(), "tei", f"{sigle}_{book_number}.xml")
    path_temp_tei = os.path.join(os.getcwd(), "tei", f"{sigle}_{book_number}_temp.xml")
    path_new_tei = os.path.join(os.getcwd(), "tei", "output", f"{sigle}_{book_number}_new.xml")
    path = os.path.join(os.getcwd(), "pagexml", sigle, book_number)
    # get number of files in directory
    number_of_files = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name)) and name.endswith('.xml')])
    remaining_pbs = number_of_files
    current_element = 0
    list_of_elements_to_be_replaced = [['<g ref="#char-019a">ƚ</g>','<g ref="#char-a749">ꝉ</g>'], 
                                       ['<g ref="#char-0119">ę</g>','ę']]

    preprocess_TEI(path_tei, path_temp_tei, list_of_elements_to_be_replaced)

    tei_root = load_tei_file(path_temp_tei)
    tei_root = remove_attributes(tei_root)
    tei_root = iterate_through_pagexml(
        path, iiif_start_number, number_of_files, remaining_pbs, current_element, tei_root, sigle, book_number)

    save_xml_file(tei_root, path_new_tei)

    list_of_elements_to_be_checked =   ['<g ref="#char-f1ac"></g>',
                                        '<pc type="distinctio"><g ref="#char-f1f8"></g></pc>',
                                        '<pc type="p-versus"><g ref="#char-f1ea"></g></pc>',
                                        '<pc type="p-flexus"><g ref="#char-f1f5"></g></pc>',
                                        '<pc type="p-comma-positura"><g ref="#char-f1e4"></g></pc>',
                                        '<pc type="p-elevatus"><g ref="#char-f1f0"></g></pc>',
                                        '<pc type="p-interrogativus"><g ref="#char-f160"></g></pc>',
                                        '<pc type="p-interrogativus-positura"><g ref="#char-int-posit"></g></pc>',
                                        '<g ref="#char-f1e1"></g>',
                                        '<g ref="#char-0180">ƀ</g>',
                                        '<g ref="#char-0111">đ</g>',
                                        '<g ref="#char-0127">ħ</g>',
                                        '<g ref="#char-f1c2"></g>',
                                        '<g ref="#char-a740">Ꝁ</g>',
                                        '<g ref="#char-a741">ꝁ</g>',
                                        '<g ref="#char-a748">Ꝉ</g>',
                                        '<g ref="#char-a749">ꝉ</g>',
                                        '<g ref="#char-019a">ƚ</g>',
                                        '<g ref="#char-0119">ę</g>',
                                        '<g ref="#char-a750">Ꝑ</g>',
                                        '<g ref="#char-a751">ꝑ</g>',
                                        '<g ref="#char-a752">Ꝓ</g>',
                                        '<g ref="#char-a753">ꝓ</g>',
                                        '<g ref="#char-0304">&#x0304;</g>',
                                        '<g ref="#char-0305">&#x0305;</g>',
                                        '<g ref="#char-a757">ꝗ</g>',
                                        '<g ref="#char-a759">ꝙ</g>',
                                        '<g ref="#char-a75D">ꝝ</g>',
                                        '<g ref="#char-a75C">Ꝝ</g>',
                                        '<g ref="#char-1dd2">&#x1dd2;</g>',
                                        '<g ref="#char-1dd3">&#x1dd3;</g>',
                                        '<g ref="#char-0365">&#x0365;</g>',
                                        '<g ref="#char-0300">◌̀</g>',
                                        '<g ref="#char-0301">◌́</g>',
                                        '<g ref="#char-0302">◌̂</g>',
                                        '<g ref="#char-0306">◌̆</g>',
                                        '<g ref="#char-0366">◌ͦ</g>',
                                        '<g ref="#char-0367">◌ͧ</g>',
                                        '<g ref="#char-211E">℞</g>',
                                        '<g ref="#char-a756">Ꝗ</g>',
                                        '<g ref="#char-a758">Ꝙ</g>',
                                        '<g ref="#char-2234">∴</g>',
                                        '<g ref="#char-23D1">⏑</g>']

    postprocess_TEI(path_new_tei, list_of_elements_to_be_checked)


"""
def main():
    sigle = "F"
    # variables
    path_tei = os.path.join(os.getcwd(), "tei", f"{sigle}_13.xml")
    path_new_tei = os.path.join(os.getcwd(), "tei", f"{sigle}_13_new.xml")
    path = os.path.join(os.getcwd(), "pagexml", sigle, "01")
    iiif_start_number = 2036028
    # get number of files in directory
    # number_of_files = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    number_of_files = 7
    remaining_pbs = number_of_files
    current_element = 0

    tei_root = load_tei_file(path_tei)
    tei_root = remove_attributes(tei_root)
    tei_root = iterate_through_pagexml(
        path, iiif_start_number, number_of_files, remaining_pbs, current_element, tei_root)

    save_xml_file(tei_root, path_new_tei)
"""

#if __name__ == "__main__":
 #   main()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Given the sigle and book number, the function adds the ids")
    parser.add_argument("-S", "--sigle", help="Book sigle", required=True)
    parser.add_argument("-B", "--book-number", help="Book number", required=True)
    parser.add_argument("-N", "--iiif-start-number", help="IIIF start number", required=True)

    args = parser.parse_args()
    main(args.sigle, args.book_number, args.iiif_start_number)
    #python bdd_coordinates.py -S F -B 13
"""
2036028
F = https://sammlungen.ub.uni-frankfurt.de/i3f/v20/{2036028}/full/full/0/default.jpg -> 412

TODO: white space -> might be a problem with <pc> in chapter_number -> e, ende durch jede textregion ohne fw und chaptercount durch und von hand ersetzen
TODO: prüfmodus
TODO: F korrigieren, verschiedene ... haben kein unclear etc.
TODO: für andere handschriften vorbereiten

"""
