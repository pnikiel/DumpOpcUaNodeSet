from lxml import etree

from pyuaf.util import Address, ExpandedNodeId, NodeId
from pyuaf.util import constants, opcuaidentifiers, nodeididentifiertypes

from stringify import stringify_nodeid

import pdb

def initialize_document():
    nsmap = {}
    nsmap[None] = 'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd'
    root = etree.Element("UANodeSet", nsmap=nsmap )
    namespaceUris = etree.Element("NamespaceUris")
    uri = etree.Element("Uri")
    uri.text = "http://fix-your-company-name-here.org/MyProject/"  #  TODO namespace mapping should come from outside
    namespaceUris.append(uri)
    root.append(namespaceUris)

    return root

def writeout_document(document, path):
    output_file = file(path, 'w')  #  TODO: path should be configurable
    output_file.write( etree.tostring(document, pretty_print=True, xml_declaration=True, encoding='utf8') )

def make_element_for_references(references, parent, refTypeFromParent):
    if len(references)>0 or parent.nodeId().nameSpaceIndex() == 0L:  # TODO constant
        element_references = etree.Element("References")
        if parent.nodeId().nameSpaceIndex() == 0L:
            root_ref = etree.Element("Reference", ReferenceType=stringify_nodeid(refTypeFromParent), IsForward="false")
            root_ref.text = stringify_nodeid( parent.nodeId() )
            element_references.append(root_ref)
        for reference in references:
            #pdb.set_trace()
            element_reference = etree.Element("Reference", ReferenceType=stringify_nodeid( reference.referenceTypeId ))
            element_reference.text = stringify_nodeid( reference.nodeId.nodeId() )
            element_references.append(element_reference)
            print reference
        return element_references
    else:
        return None

def make_element(nodeid, opcua_attributes, references, parent, refTypeFromParent, AttributesOfObject, ElementsOfObject, type_name):
    attributes = {k:str(v) for k,v in opcua_attributes.iteritems() if k in AttributesOfObject}
    extra_elements = {k:v for k,v in opcua_attributes.iteritems() if k in ElementsOfObject}
    element = etree.Element(type_name, attributes)

    for key in extra_elements.keys():
        extra_element = etree.Element(key)
        extra_element.text = extra_elements[key]
        element.append (extra_element)
    potential_references = make_element_for_references(references, parent, refTypeFromParent)
    if (potential_references):
        element.append(potential_references)
        
    return element


def make_element_for_uaobject(nodeid, opcua_attributes, references, parent, refTypeFromParent):
    AttributesOfObject = ['NodeId', 'BrowseName']
    ElementsOfObject = ['DisplayName']
    return make_element(nodeid, opcua_attributes, references, parent, refTypeFromParent, AttributesOfObject, ElementsOfObject, 'UAObject')

def make_element_for_uavariable(nodeid, opcua_attributes, references, parent, refTypeFromParent):
    AttributesOfVariable = ['NodeId', 'BrowseName', 'DataType', 'ValueRank', 'ArrayDimensions', 'AccessLevel', 'UserAccessLevel', 'MinimumSamplingInterval', 'Historizing']
    ElementsOfVariable = ['DisplayName', 'Value']
    return make_element(nodeid, opcua_attributes, references, parent, refTypeFromParent, AttributesOfVariable, ElementsOfVariable, 'UAVariable')

def make_element_for_uamethod(nodeid, opcua_attributes, references, parent, refTypeFromParent):
    AttributesOfMethod = ['NodeId', 'BrowseName', 'Executable']
    ElementsOfMethod = ['DisplayName']  # TODO MethodArgument missing!
    return make_element(nodeid, opcua_attributes, references, parent, refTypeFromParent, AttributesOfMethod, ElementsOfMethod, 'UAMethod')

