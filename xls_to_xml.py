from pathlib import Path
import xlrd
import msoffcrypto
import xml.etree.ElementTree as ET
import datetime


# Indent XML into a beautified format
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def verify_input(text: str):
    return text.replace('"', '&quot;').replace('&', '&amp;').replace('>', '&gt;').\
        replace('<', '&lt;').replace('\'', '&apos;')


def build_tree(file_name: Path, worksheet, shop_info: dict, categories: dict):
    catalogue = ET.Element('yml_catalog', date=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
    shop = ET.SubElement(catalogue, 'shop')
    ET.SubElement(shop, 'name').text = shop_info['name']
    ET.SubElement(shop, 'company').text = shop_info['company']
    ET.SubElement(shop, 'url').text = shop_info['url']
    shop_currencies = ET.SubElement(shop, 'currencies')
    for currency in shop_info['currencies']:
        for cur_id, cur_rate in currency.items():
            ET.SubElement(shop_currencies, 'currency', id=cur_id, rate=cur_rate)
    categories_section = ET.SubElement(shop, 'categories')
    for cat_name, cat_id in categories.items():
        ET.SubElement(categories_section, 'category', id=cat_id).text = cat_name
    # shipment_options = ET.SubElement(shop, 'shipment-options')
    offers = ET.SubElement(shop, "offers")

    for product in [worksheet.row_values(i) for i in range(2, worksheet.nrows)]:
        print(product)
        available = 'true' if product[1] == 'В наличии' or product[1] is None else 'false'
        offer = ET.SubElement(offers, 'offer', id=str(int(product[0])), available=available)
        ET.SubElement(offer, 'url').text = product[7]
        ET.SubElement(offer, 'name').text = verify_input(product[9])
        ET.SubElement(offer, 'price').text = verify_input(str(product[11]))
        ET.SubElement(offer, 'categoryId').text = categories[product[10]]
        ET.SubElement(offer, 'picture').text = product[14]
        ET.SubElement(offer, 'vendor').text = verify_input(product[8])
        ET.SubElement(offer, 'description').text = verify_input(product[15])
    indent(catalogue)

    tree = ET.ElementTree(catalogue)
    tree.write(file_name, xml_declaration=True, encoding='utf-8', method="xml")


def read_files(path: Path, file_types: tuple):
    if path.is_dir():
        input_files = [item for item in path.iterdir() if item.name.endswith(file_types)]
        return input_files
    return False


if __name__ == "__main__":
    # Settings
    # Список категорий в формате {'name1': 'id1', 'name2': 'id2', etc}
    product_categories = {'Суперфуды': '1', 'Масло растительное': '2'}

    # Информация о подключаемом магазине (компании)
    shop_information = {
        'name': 'Vitavim',
        'company': 'ООО "Жизнь"',
        'url': 'https://vitavim.ru/',
        'currencies': [
            {'RUR': '1'}
        ]
    }

    # Количество товаров конвертируемых в xml, 0 - без ограничения
    products_limit = 0

    project_dir_path = Path(__file__).parent
    project_input_dir = project_dir_path / 'in'
    project_results_dir = project_dir_path / 'out'
    Path(project_results_dir).mkdir(exist_ok=True)
    decrypted = project_input_dir / 'decrypted.xls'

    types = ('.xls', '.xlsx')
    files_grabbed = read_files(project_input_dir, types)

    for f in files_grabbed:
        output_xml = project_results_dir / (str(datetime.datetime.now().date()) + '_' + f.name.split('.')[0] + '.xml')
        try:
            with xlrd.open_workbook(f) as wb:
                sheets = wb.sheet_names()
        except xlrd.biffh.XLRDError as err:
            print('File is encrypted.', err)
            wb_msoffcrypto_file = msoffcrypto.OfficeFile(open(f, 'rb'))
            wb_msoffcrypto_file.load_key(password='VelvetSweatshop')
            print('Worked Password')
            wb_msoffcrypto_file.decrypt(open(decrypted, 'wb'))
            with xlrd.open_workbook(decrypted) as wb:
                sheets = wb.sheet_names()

        print(sheets)
        if len(sheets) < 2:
            sheet = wb.sheet_by_name(sheets[0])
        else:
            sheet = wb.sheet_by_index(2)

        if sheet.nrows > 2:
            build_tree(output_xml, sheet, shop_information, product_categories)
        if decrypted.exists():
            decrypted.unlink()
