from helpers import process_request, download_pdf

url = 'http://www.manualsonline.com'
counter = 0
soup = process_request(url)


# Define when pagination pages are over
def define_step_link(links):
    for link in links:
        childs = link.children
        for child in childs:
            if child.get('class')[1] == 'fa-chevron-right':
                return link


# Extract subcategory links
def parse_single_page(base_link, soup,  selector):
    links = []
    for link in soup.select(selector):
        links.append(base_link + link.get('href'))
    return links


# Recursive parsing function. Heart of logic
def parser(soup, third_level_links, selector):
    links_per_page = parse_single_page(view_all_links[1],
                                           soup, selector)
    third_level_links += links_per_page
    if len(links_per_page) < 50:
        return third_level_links

    step_link = define_step_link(soup.select('.step-links > a'))
    target_link = view_all_links[1][0:-1] + step_link.get('href')
    soup = process_request(target_link)
    return parser(soup, third_level_links, selector)

view_all_links = []
for link in soup.select('.category_viewall a'):
    view_all_links.append(link.get('href'))

for base_link in view_all_links:
    soup = process_request(base_link)
    second_level_links = parser(soup, [], '.seeprices-header a')

    for second_level_link in second_level_links:
        soup = process_request(second_level_link)
        third_level_links = parser(soup, [], '.seeprices-header a')

        for third_level_link in third_level_links:
            soup = process_request(third_level_link)
            fourth_level_links = parser(soup, [], '.letter-img a')
            link_names = soup.select('.product-list .cat-list-row .col-md-8 h5 a')

            for link, link_name in zip(fourth_level_links, link_names):
                soup = process_request(link)
                target_links = parser(soup, [], '.pdf-viewer .html-controls .ctrl-btn-pdf')
                for target_link in target_links:
                    target_link = target_link.replace(view_all_links[1], '')
                    counter += 1
                    print(target_link, ' : ', counter)
                    download_pdf(target_link, link_name)









