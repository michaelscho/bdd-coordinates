manuscript_data = { 'F': {
                        'signatur': 'Frankfurt a.M., UB, Barth. 50',
                        'transkribus_collection_id': 80437,
                        'transkribus_document_id': 637541,
                        'base_folder': '01_Transkription_Frankfurt-ub-b-50',
                        'tei_base_id': 'frankfurt-ub-b-50-',
                        'iiif_scale_factor': 1.34,
                        'iiif_start_number': 2036028,
                        'facs_url':'f"https://sammlungen.ub.uni-frankfurt.de/i3f/v20/{self.iiif_image_id}/full/full/0/default.jpg"',
                        'corresp':'f"https://sammlungen.ub.uni-frankfurt.de/msma/i3f/v20/2035614/canvas/{self.iiif_image_id}"',
                        'ana':'f"/annotations/frankfurt-ub-b-50-annotation-{self.iiif_image_id}"'},

                    'B': {
                        'signatur': 'Bamberg, SB, Can. 6',
                        'transkribus_collection_id': 80437,
                        'transkribus_document_id': 732612,
                        'base_folder': '01_Transkription_Bamberg_Stabi_Can_6',
                        'tei_base_id': 'bamberg-sb-c-6-',
                        'iiif_scale_factor': 1,
                        'iiif_start_number': 410,
                        'facs_url':'f"https://api.digitale-sammlungen.de/iiif/image/v2/bsb00140701_00{self.iiif_image_id}/full/full/0/default.jpg"',
                        'corresp':'f"https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb00140701/canvas/{self.iiif_image_id}"',
                        'ana':'f"/annotations/bamberg-sb-c-6-annotation-{self.iiif_image_id}"'},

                    'K': {
                        'signatur': 'Köln, EDD, Cod. 119',
                        'transkribus_collection_id': 80437,
                        'transkribus_document_id': 796594,
                        'base_folder': '01_Transkription_Köln_EDD_Cod_119',
                        'tei_base_id': 'koeln-edd-c-119-',
                        'iiif_scale_factor': 1,
                        'iiif_start_number': 284583, #check
                        'facs_url':'f"https://digital.dombibliothek-koeln.de/i3f/v20/{self.iiif_image_id}/full/full/0/default.jpg"',
                        'corresp':'f"https://digital.dombibliothek-koeln.de/i3f/v20/284343/canvas/{self.iiif_image_id}"',
                        'ana':'f"/annotations/koeln-edd-c-119-annotation-{self.iiif_image_id}"'},

                    'Va': {
                        'signatur': 'Vatikan, BAV, Pal. lat. 585',
                        'transkribus_collection_id': 80437,
                        'transkribus_document_id': 855714,
                        'base_folder': '01_Transkription_BAV_Pal_lat_585',
                        'tei_base_id': 'vatican-bav-pal-lat-585-',
                        'iiif_scale_factor': 1,
                        'iiif_start_number': 2036028, # cannot find
                        'facs_url':'f"https://digi.vatlib.it/pub/digit/MSS_Pal.lat.585/iiif/Pal.lat.585_{str(self.iiif_image_id).zfill(4)}_fa_{self.start_folio[:-1].zfill(4)+self.start_folio[-1:]}.jp2/full/full/0/default.jpg"',
                        'corresp':'f"https://digi.vatlib.it/iiif/MSS_Pal.lat.585/canvas/p{str(self.iiif_image_id).zfill(4)}"',
                        'ana':'f"/annotations/vatican-bav-pal-lat-585-annotation-p{str(self.iiif_image_id).zfill(4)}"'},

                    'Vb': {
                        'signatur': 'Vatikan, BAV, Pal. lat. 586',
                        'transkribus_collection_id': 80437,
                        'transkribus_document_id': 1197208,
                        'base_folder': '01_Transkription_BAV_Pal_lat_586',
                        'tei_base_id': 'vatican-bav-pal-lat-586-',
                        'iiif_scale_factor': 1,
                        'iiif_start_number': 2036028, # cannot find
                        'facs_url':'f"https://digi.vatlib.it/pub/digit/MSS_Pal.lat.585/iiif/Pal.lat.586_{str(self.iiif_image_id).zfill(4)}_fa_{self.start_folio[:-1].zfill(4)+self.start_folio[-1:]}.jp2/full/full/0/default.jpg"',
                        'corresp':'f"https://digi.vatlib.it/iiif/MSS_Pal.lat.586/canvas/p{str(self.iiif_image_id).zfill(4)}"',
                        'ana':'f"/annotations/vatican-bav-pal-lat-586-annotation-p{str(self.iiif_image_id).zfill(4)}"'},
}