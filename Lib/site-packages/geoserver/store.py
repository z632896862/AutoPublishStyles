# coding: utf-8

from urllib.parse import urljoin

from geoserver import settings
from geoserver.resource import featuretype_from_index, \
    coverage_from_index, wmslayer_from_index
from geoserver.workspace import Workspace
from geoserver.support import ResourceInfo, xml_property, \
    key_value_pairs, write_bool, write_dict, write_string


def datastore_from_index(catalog, workspace, node):
    name = node.find("name")
    return DataStore(catalog, workspace, name.text)


def coveragestore_from_index(catalog, workspace, node):
    name = node.find("name")
    return CoverageStore(catalog, workspace, name.text)


def wmsstore_from_index(catalog, workspace, node):
    name = node.find("name")
    # user = node.find("user")
    # password = node.find("password")
    return WmsStore(catalog, workspace, name.text)


class DataStore(ResourceInfo):
    resource_type = "dataStore"
    save_method = settings.PUT

    def __init__(self, catalog, workspace, name):
        super(DataStore, self).__init__()
        assert isinstance(workspace, Workspace)
        assert isinstance(name, str)
        self.catalog = catalog
        self.workspace = workspace
        self.name = name

    @property
    def href(self):
        join_url = "workspaces/{}/datastores/{}.xml".format(
            self.workspace.name,
            self.name
        )
        return urljoin(self.catalog.service_url, join_url)

    enabled = xml_property("enabled", lambda x: x.text == "true")
    name = xml_property("name")
    type = xml_property("type")
    connection_parameters = xml_property("connectionParameters",
                                         key_value_pairs)

    writers = {
        'enabled': write_bool("enabled"),
        'name': write_string("name"),
        'type': write_string("type"),
        'connectionParameters': write_dict("connectionParameters"),
    }

    @property
    def resource_url(self):
        return urljoin(
            self.catalog.service_url,
            "workspaces/{}/datastores/{}/featuretypes.xml".format(
                self.workspace.name,
                self.name
            )
        )

    def get_resources(self, name=None, available=False):
        res_url = self.resource_url
        if available:
            res_url += "?list=available"
        xml = self.catalog.get_xml(res_url)

        def ft_from_node(node):
            return featuretype_from_index(
                self.catalog,
                self.workspace,
                self,
                node
            )

        # if name passed, return only one FeatureType,
        # otherwise return all FeatureTypes in store:
        if name is not None:
            for node in xml.findall("featureType"):
                if node.findtext("name") == name:
                    return ft_from_node(node)
            return None
        if available:
            return [str(node.text) for node in xml.findall("featureTypeName")]
        else:
            return [ft_from_node(node) for node in xml.findall("featureType")]


class UnsavedDataStore(DataStore):
    save_method = settings.POST

    def __init__(self, catalog, name, workspace):
        super(UnsavedDataStore, self).__init__(catalog, workspace, name)
        self.dirty.update({
            'name': name,
            'enabled': True,
            'type': None,
            'connectionParameters': dict(),
        })

    @property
    def href(self):
        return urljoin(
            self.catalog.service_url,
            "workspaces/{}/datastores/?name={}".format(
                self.workspace.name,
                self.name
            )
        )


class CoverageStore(ResourceInfo):
    resource_type = 'coverageStore'
    save_method = settings.PUT

    def __init__(self, catalog, workspace, name):
        super(CoverageStore, self).__init__()
        assert isinstance(workspace, Workspace)
        assert isinstance(name, str)
        self.catalog = catalog
        self.workspace = workspace
        self.name = name

    @property
    def href(self):
        return urljoin(
            self.catalog.service_url,
            "workspaces/{}/coveragestores/{}.xml".format(
                self.workspace.name,
                self.name,
            )
        )

    enabled = xml_property("enabled", lambda x: x.text == "true")
    name = xml_property("name")
    url = xml_property("url")
    type = xml_property("type")

    writers = {
        'enabled': write_bool("enabled"),
        'name': write_string("name"),
        'url': write_string("url"),
        'type': write_string("type"),
        'workspace': write_string("workspace")
    }

    def get_resources(self, name=None):
        res_url = urljoin(
            self.catalog.service_url,
            "workspaces/{}/coveragestores/{}/coverages.xml".format(
                self.workspace.name,
                self.name
            )
        )
        xml = self.catalog.get_xml(res_url)

        def cov_from_node(node):
            return coverage_from_index(
                self.catalog,
                self.workspace,
                self,
                node
            )

        # if name passed, return only one Coverage,
        # otherwise return all Coverages in store:
        if name is not None:
            for node in xml.findall("coverage"):
                if node.findtext("name") == name:
                    return cov_from_node(node)
            return None
        return [cov_from_node(node) for node in xml.findall("coverage")]


class UnsavedCoverageStore(CoverageStore):
    save_method = settings.POST

    def __init__(self, catalog, name, workspace):
        super(UnsavedCoverageStore, self).__init__(catalog, workspace, name)
        self.dirty.update({
            'name': name,
            'enabled': True,
            'type': "GeoTIFF",
            'url': "file:data/",
            'workspace': workspace.name if workspace else None
        })

    @property
    def href(self):
        return urljoin(
            self.catalog.service_url,
            "workspaces/{}/coveragestores/?name={}".format(
                self.workspace.name,
                self.name
            )
        )


class WmsStore(ResourceInfo):
    resource_type = "wmsStore"
    save_method = settings.PUT

    def __init__(self, catalog, workspace, name):
        super(WmsStore, self).__init__()
        assert isinstance(workspace, Workspace)
        assert isinstance(name, str)
        self.catalog = catalog
        self.workspace = workspace
        self.name = name

    @property
    def href(self):
        return urljoin(
            self.catalog.service_url,
            "workspaces/{}/wmsstores/{}.xml".format(
                self.workspace.name,
                self.name
            )
        )

    enabled = xml_property("enabled", lambda x: x.text == "true")
    name = xml_property("name")
    nativeName = xml_property("nativeName")
    capabilitiesURL = xml_property("capabilitiesURL")
    type = xml_property("type")

    writers = {
        'enabled': write_bool("enabled"),
        'name': write_string("name"),
        'capabilitiesURL': write_string("capabilitiesURL"),
        'type': write_string("type"),
    }

    def get_resources(self, name=None, available=False):
        res_url = urljoin(
            self.catalog.service_url,
            "workspaces/{}/wmsstores/{}/wmslayers.xml".format(
                self.workspace.name,
                self.name
            )
        )
        layer_name_attr = "wmsLayer"
        if available:
            res_url += "?list=available"
            layer_name_attr += 'Name'
        xml = self.catalog.get_xml(res_url)

        def wl_from_node(node):
            return wmslayer_from_index(self.catalog, self.workspace, self, node)

        # if name passed, return only one layer,
        # otherwise return all layers in store:
        if name is not None:
            for node in xml.findall(layer_name_attr):
                if node.findtext("name") == name:
                    return wl_from_node(node)
            return None

        if available:
            return [str(node.text) for node in xml.findall(layer_name_attr)]
        else:
            return [wl_from_node(node) for node in xml.findall(layer_name_attr)]


class UnsavedWmsStore(WmsStore):
    save_method = settings.POST

    def __init__(self, catalog, name, workspace):
        super(UnsavedWmsStore, self).__init__(
            catalog,
            workspace,
            name,
        )
        self.dirty.update({
            'name': name,
            'enabled': True,
            'capabilitiesURL': "",
            'type': "WMS",
        })

    @property
    def href(self):
        return urljoin(
            self.catalog.service_url,
            "workspaces/{}/wmsstores/?name={}".format(
                self.workspace.name,
                self.name
            )
        )
