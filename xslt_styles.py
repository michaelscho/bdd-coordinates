abbr_xslt = """<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">

                <xsl:template match="text()">
                    <xsl:value-of select="normalize-space()"/>
                </xsl:template>


                <!-- Output as plain text -->
                <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

                <xsl:strip-space elements="subst del add"/>

                <!-- Template for the root (or any unmatched elements) -->
                <xsl:template match="/">
                    <!-- Apply templates to all child nodes -->
                    <xsl:apply-templates/>
                </xsl:template>

                <!-- Template to match <abbr> elements -->
                <xsl:template match="tei:abbr">
                    <xsl:text> </xsl:text>
                    <!-- Output the text of the <abbr> element -->
                    <xsl:apply-templates/>
                    <xsl:text>++</xsl:text>

                </xsl:template>

                <!-- Template to ignore <expan> elements -->
                <xsl:template match="tei:expan"/>

                <!-- Template to ignore other elements -->
                <xsl:template match="*">
                    <!-- Apply templates to child nodes of these elements -->
                    <xsl:apply-templates/>
                </xsl:template>

                <!-- Template to ignore other elements -->
                <xsl:template match="pc">
                    <!-- Apply templates to child nodes of these elements -->
                    <xsl:text>+</xsl:text>
                    <xsl:apply-templates/>
                    <xsl:text> </xsl:text>
                </xsl:template>

                <!-- Template to match <unclear> elements -->
<xsl:template match="tei:unclear">
    <!-- Output the special character at the beginning -->
    <xsl:text>§</xsl:text>

    <!-- Output the content of the <unclear> element -->
    <xsl:apply-templates/>

    <!-- Output the special character at the end -->
    <xsl:text>ß</xsl:text>
</xsl:template>

            </xsl:stylesheet>

                
            """

expan_xslt = """<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">

                <!-- Output as plain text -->
                <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

                <xsl:template match="text()">
    <xsl:value-of select="normalize-space()"/>
</xsl:template>


                <xsl:strip-space elements="subst del add"/>
                
                <!-- Template for the root (or any unmatched elements) -->
                <xsl:template match="/">
                    <!-- Apply templates to all child nodes -->
                    <xsl:apply-templates/>
                </xsl:template>

                <!-- Template to match <expan> elements -->
                <xsl:template match="tei:expan">
                    <!-- Output the text of the <expan> element -->
                    <xsl:text> </xsl:text>
                    <xsl:apply-templates/>
                    <xsl:text>++</xsl:text>
                </xsl:template>

                <!-- Template to ignore <abbr> elements -->
                <xsl:template match="tei:abbr"/>
                                <!-- Template to ignore other elements -->
                <xsl:template match="pc">
                    <!-- Apply templates to child nodes of these elements -->
                    <xsl:text>+</xsl:text>
                    <xsl:apply-templates/>
                    <xsl:text> </xsl:text>
                </xsl:template>
                
                <!-- Template to ignore other elements -->
                <xsl:template match="*">
                    <!-- Apply templates to child nodes of these elements -->
                    <xsl:apply-templates/>
                    </xsl:template>

                    <!-- Template to match <unclear> elements -->
<xsl:template match="tei:unclear">
    <!-- Output the special character at the beginning -->
    <xsl:text>§</xsl:text>

    <!-- Output the content of the <unclear> element -->
    <xsl:apply-templates/>

    <!-- Output the special character at the end -->
    <xsl:text>ß</xsl:text>
</xsl:template>

                </xsl:stylesheet>
            """

abbr_xslt_for_lines = """
                            <xsl:stylesheet version="2.0"
                                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                                xmlns:tei="http://www.tei-c.org/ns/1.0"
                                xmlns:xml="http://www.w3.org/XML/1998/namespace">

                                <xsl:template match="text()">
    <xsl:value-of select="normalize-space()"/>
</xsl:template>

                                
                            <!-- Output as plain text -->
                            <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

                            <xsl:strip-space elements="subst del add"/>

                            <!-- Template for the root (or any unmatched elements) -->
                            <xsl:template match="/">
                                <!-- Apply templates to all child nodes -->
                                <xsl:apply-templates/>
                            </xsl:template>

                            <!-- nur Kindelemente von 'body' auswerten -->
                            <xsl:template match="tei:TEI">
                                <xsl:apply-templates select="tei:text/tei:body/*"/>
                            </xsl:template>     

                                            <!-- Template to ignore other elements -->
                <xsl:template match="pc">
                    <!-- Apply templates to child nodes of these elements -->
                    <xsl:text>+</xsl:text>
                    <xsl:apply-templates/>
                    <xsl:text> </xsl:text>
                </xsl:template>                       

                            <!-- create lbs as \n and ¬\n -->                            
                            <xsl:template match="tei:lb">
                                <xsl:text>#</xsl:text>
                                <xsl:value-of select="@xml:id"/>
                                <xsl:text>|</xsl:text>  
                            </xsl:template>

                            <!--
                            <xsl:template match="tei:lb[break='no']">
                                <xsl:text>¬#</xsl:text>
                                <xsl:value-of select="@xml:id"/>
                                <xsl:text>|</xsl:text>
                            </xsl:template>
                            -->
                            
                            <!-- Template to match <abbr> elements -->
                            <xsl:template match="tei:abbr">
                                <!-- Output the text of the <abbr> element -->
                                <xsl:text> </xsl:text>
                                <xsl:apply-templates/>
                                <xsl:text>++</xsl:text>
                            </xsl:template>

                            <!-- Template to ignore <expan> elements -->
                            <xsl:template match="tei:expan">
                            </xsl:template>

                            <!-- Template to ignore <fw> elements -->
                            <xsl:template match="tei:fw">
                            </xsl:template>

                            <xsl:template match="tei:note">
                            </xsl:template>
                            
                            <xsl:template match="tei:label">
                            </xsl:template>
                            
                            <xsl:template match="tei:teiHeader">
                            </xsl:template>

                            <!-- supplied ohne Leerzeichen -->
                            <xsl:template match="tei:supplied">
                            </xsl:template>

                            <!-- supplied ohne Leerzeichen -->
                            <xsl:template match="tei:del">
                            </xsl:template>

                            <!-- Template to match <unclear> elements -->
<xsl:template match="tei:unclear">
    <!-- Output the special character at the beginning -->
    <xsl:text>§</xsl:text>

    <!-- Output the content of the <unclear> element -->
    <xsl:apply-templates/>

    <!-- Output the special character at the end -->
    <xsl:text>ß</xsl:text>
</xsl:template>

<xsl:template match="subst">
    <!-- Process the delete element if necessary -->
    <xsl:apply-templates select="del"/>

    <!-- Add the text from the add element -->
    <xsl:value-of select="add"/>
</xsl:template>

<xsl:template match="del">
    <!-- You can choose to ignore this, or handle it specially -->
</xsl:template>


                            
                    </xsl:stylesheet>

                        """

expan_xslt_for_lines = """
                            <xsl:stylesheet version="2.0"
                                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                                xmlns:tei="http://www.tei-c.org/ns/1.0"
                                xmlns:xml="http://www.w3.org/XML/1998/namespace">

                                <xsl:template match="text()">
    <xsl:value-of select="normalize-space()"/>
</xsl:template>

                                
                            <!-- Output as plain text -->
                            <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

                            <xsl:strip-space elements="subst del add"/>

                            <!-- Template for the root (or any unmatched elements) -->
                            <xsl:template match="/">
                                <!-- Apply templates to all child nodes -->
                                <xsl:apply-templates/>
                            </xsl:template>

                            <!-- nur Kindelemente von 'body' auswerten -->
                            <xsl:template match="tei:TEI">
                                <xsl:apply-templates select="tei:text/tei:body/*"/>
                            </xsl:template> 

                                            <!-- Template to ignore other elements -->
                <xsl:template match="pc">
                    <!-- Apply templates to child nodes of these elements -->
                    <xsl:text>+</xsl:text>
                    <xsl:apply-templates/>
                    <xsl:text> </xsl:text>
                </xsl:template>                           

                            <!-- create lbs as \n and ¬\n -->                            
                            <xsl:template match="tei:lb">
                                <xsl:text>#</xsl:text>
                                <xsl:value-of select="@xml:id"/>
                                <xsl:text>|</xsl:text>  
                            </xsl:template>
                            
                            <!--
                            <xsl:template match="tei:lb[break='no']">
                                <xsl:text>¬#</xsl:text>
                                <xsl:value-of select="@xml:id"/>
                                <xsl:text>|</xsl:text>
                            </xsl:template>
                            -->

                            <!-- Template to match <expan> elements -->
                            <xsl:template match="tei:expan">
                                <!-- Output the text of the <expan> element -->
                                <xsl:text> </xsl:text>
                                <xsl:apply-templates/>
                                <xsl:text>++</xsl:text>

                            </xsl:template>

                            <!-- Template to ignore <abbr> elements -->
                            <xsl:template match="tei:abbr">
                            </xsl:template>

                            <!-- Template to ignore <fw> elements -->
                            <xsl:template match="tei:fw">
                            </xsl:template>

                            <xsl:template match="tei:note">
                            </xsl:template>
                            
                            <xsl:template match="tei:label">
                            </xsl:template>
                            
                            <xsl:template match="tei:teiHeader">
                            </xsl:template>

                            <!-- supplied ohne Leerzeichen -->
                            <xsl:template match="tei:supplied">
                            </xsl:template>

                            <!-- supplied ohne Leerzeichen -->
                            <xsl:template match="tei:del">
                            </xsl:template>

                            <!-- Template to match <unclear> elements -->
<xsl:template match="tei:unclear">
    <!-- Output the special character at the beginning -->
    <xsl:text>§</xsl:text>

    <!-- Output the content of the <unclear> element -->
    <xsl:apply-templates/>

    <!-- Output the special character at the end -->
    <xsl:text>ß</xsl:text>
</xsl:template>

<xsl:template match="subst">
    <!-- Process the delete element if necessary -->
    <xsl:apply-templates select="del"/>

    <!-- Add the text from the add element -->
    <xsl:value-of select="add"/>
</xsl:template>

<xsl:template match="del">
    <!-- You can choose to ignore this, or handle it specially -->
</xsl:template>


                            
                    </xsl:stylesheet>

                        """

abbr_xslt_for_lines_inscription = """
                            <xsl:stylesheet version="2.0"
                                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                                xmlns:tei="http://www.tei-c.org/ns/1.0"
                                xmlns:xml="http://www.w3.org/XML/1998/namespace">

                                <xsl:template match="text()">
                                    <xsl:value-of select="normalize-space()"/>
                                </xsl:template>


                                <xsl:strip-space elements="subst del add"/>
                                
                                <!-- Output as plain text -->
                                <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

                                <!-- Template for the root (or any unmatched elements) -->
                                <xsl:template match="/">
                                    <!-- Apply templates to all child nodes -->
                                    <xsl:apply-templates/>
                                </xsl:template>

                                <!-- nur inscription auswerten -->
                                <xsl:template match="tei:TEI">
                                    <xsl:apply-templates select="tei:text/tei:body//tei:note[@type='inscription']/node()"/>
                                </xsl:template>  

                                <!-- Template to ignore other elements -->
                                <xsl:template match="pc">
                                    <!-- Apply templates to child nodes of these elements -->
                                    <xsl:text>+</xsl:text>
                                    <xsl:apply-templates/>
                                    <xsl:text> </xsl:text>
                                </xsl:template>                          

                                <!-- create lbs as \n and ¬\n -->                            
                                <xsl:template match="tei:lb">
                                    <xsl:text>#</xsl:text>
                                    <xsl:value-of select="@xml:id"/>
                                    <xsl:text>|</xsl:text>  
                                </xsl:template>
                            
                                <!--
                                <xsl:template match="tei:lb[break='no']">
                                    <xsl:text>¬#</xsl:text>
                                    <xsl:value-of select="@xml:id"/>
                                    <xsl:text>|</xsl:text>
                                </xsl:template>
                                -->

                                <!-- Template to match <abbr> elements -->
                                <xsl:template match="tei:abbr">
                                    <!-- Output the text of the <abbr> element -->
                                    <xsl:text> </xsl:text>
                                    <xsl:apply-templates/>
                                    <xsl:text>++</xsl:text>
                                </xsl:template>

                                <!-- Template to ignore <expan> elements -->
                                <xsl:template match="tei:expan">
                                </xsl:template>

                                <!-- Template to ignore <fw> elements -->
                                <xsl:template match="tei:fw">
                                </xsl:template>

                                <xsl:template match="tei:note">
                                </xsl:template>

                                <xsl:template match="tei:label">
                                </xsl:template>

                                <xsl:template match="tei:teiHeader">
                                </xsl:template>

                                <!-- supplied ohne Leerzeichen -->
                                <xsl:template match="tei:supplied">
                                </xsl:template>

                                <!-- supplied ohne Leerzeichen -->
                                <xsl:template match="tei:del">
                                </xsl:template>

                                <!-- Template to match <unclear> elements -->
                                <xsl:template match="tei:unclear">
                                    <!-- Output the special character at the beginning -->
                                    <xsl:text>§</xsl:text>

                                    <!-- Output the content of the <unclear> element -->
                                    <xsl:apply-templates/>

                                    <!-- Output the special character at the end -->
                                    <xsl:text>ß</xsl:text>
                                </xsl:template>

                                <xsl:template match="subst">
                                    <!-- Process the delete element if necessary -->
                                    <xsl:apply-templates select="del"/>

                                    <!-- Add the text from the add element -->
                                    <xsl:value-of select="add"/>
                                </xsl:template>

                                <xsl:template match="del">
                                    <!-- You can choose to ignore this, or handle it specially -->
                                </xsl:template>
                            </xsl:stylesheet>

                        """

expan_xslt_for_lines_inscription = """
                            <xsl:stylesheet version="2.0"
                                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                                xmlns:tei="http://www.tei-c.org/ns/1.0"
                                xmlns:xml="http://www.w3.org/XML/1998/namespace">

                                <xsl:template match="text()">
                                    <xsl:value-of select="normalize-space()"/>
                                </xsl:template>

                                <xsl:strip-space elements="subst del add"/>

                                <!-- Output as plain text -->
                                <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

                                <!-- Template for the root (or any unmatched elements) -->
                                <xsl:template match="/">
                                    <!-- Apply templates to all child nodes -->
                                    <xsl:apply-templates/>
                                </xsl:template>

                                <!-- nur inscription auswerten -->
                                <xsl:template match="tei:TEI">
                                    <xsl:apply-templates select="tei:text/tei:body//tei:note[@type='inscription']/node()"/>
                                </xsl:template>                            
                       
                                <!-- Template to ignore other elements -->
                                <xsl:template match="pc">
                                    <!-- Apply templates to child nodes of these elements -->
                                    <xsl:text>+</xsl:text>
                                    <xsl:apply-templates/>
                                    <xsl:text> </xsl:text>
                                </xsl:template>

                                <!-- create lbs as \n and ¬\n -->                            
                                <xsl:template match="tei:lb">
                                    <xsl:text>#</xsl:text>
                                    <xsl:value-of select="@xml:id"/>
                                    <xsl:text>|</xsl:text>  
                                </xsl:template>
                            
                                <!--
                                <xsl:template match="tei:lb[break='no']">
                                    <xsl:text>¬#</xsl:text>
                                    <xsl:value-of select="@xml:id"/>
                                    <xsl:text>|</xsl:text>
                                </xsl:template>
                                -->

                                <!-- Template to match <expan> elements -->
                                <xsl:template match="tei:expan">
                                    <!-- Output the text of the <expan> element -->
                                    <xsl:text> </xsl:text>
                                    <xsl:apply-templates/>
                                    <xsl:text>++</xsl:text>
                                </xsl:template>

                                <!-- Template to ignore <abbr> elements -->
                                <xsl:template match="tei:abbr">
                                </xsl:template>

                                <!-- Template to ignore <fw> elements -->
                                <xsl:template match="tei:fw">
                                </xsl:template>

                                <xsl:template match="tei:note">
                                </xsl:template>

                                <xsl:template match="tei:label">
                                </xsl:template>

                                <xsl:template match="tei:teiHeader">
                                </xsl:template>

                                <!-- supplied ohne Leerzeichen -->
                                <xsl:template match="tei:supplied">
                                </xsl:template>

                                <!-- supplied ohne Leerzeichen -->
                                <xsl:template match="tei:del">
                                </xsl:template>

                                <!-- Template to match <unclear> elements -->
                                <xsl:template match="tei:unclear">
                                    <!-- Output the special character at the beginning -->
                                    <xsl:text>§</xsl:text>

                                     <!-- Output the content of the <unclear> element -->
                                    <xsl:apply-templates/>

                                    <!-- Output the special character at the end -->
                                    <xsl:text>ß</xsl:text>
                                </xsl:template>

                                <xsl:template match="subst">
                                <!-- Process the delete element if necessary -->
                                    <xsl:apply-templates select="del"/>

                                    <!-- Add the text from the add element -->
                                    <xsl:value-of select="add"/>
                                </xsl:template>

                                <xsl:template match="del">
                                <!-- You can choose to ignore this, or handle it specially -->
                                </xsl:template>
                            </xsl:stylesheet>

                        """
