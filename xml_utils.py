import xml.etree.ElementTree as ET



def parse_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    component_info = {}

    for cell in root.findall('.//mxCell'):
        cell_id = cell.get('id')
        cell_value = cell.get('value')
        cell_style = cell.get('style')

        if cell_value is not None and cell_style is not None:
            component_type = None
            if "firewall" in cell_value.lower() or "firewall" in cell_style.lower():
                component_type = "Firewall"
            elif "Router" in cell_style:
                component_type = "Router"
            elif "pc" in cell_value.lower() or "pc" in cell_style.lower() or "laptop" in cell_value.lower() or "laptop" in cell_style.lower():
                component_type = "Client"
            elif "internet" in cell_value.lower() or "internet" in cell_style.lower():
                component_type = "Internet"
            elif "web" in cell_value.lower() and "server" in cell_value.lower() or "web" in cell_style.lower() and "server" in cell_style.lower():
                component_type = "WebServer" 
            elif "database" in cell_value.lower() or "database" in cell_style.lower():
                component_type = "Database"       
            elif "server" in cell_value.lower() or "server" in cell_style.lower():
                component_type = "Server"

            if component_type:
                component_info[cell_id] = {
                    'Type': component_type,

                }
            print(component_info)
            result_list = [{'Type': value['Type']} for value in component_info.values()]

    return result_list

