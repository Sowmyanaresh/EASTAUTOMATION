from typing import OrderedDict
from selenium import webdriver
import pytest
import os
import datetime, time
from pathlib import Path
from py.xml import html
import pandas as pd
from utilities.readProperties import ReadConfig
import platform,socket,psutil
from utilities.reportHtmlToXml import reportHtmlToXml
#import Helpers.testrailAPI as tr
#import xml.dom.minidom
#import glob
#from pyhtml2pdf import converter



# a useful primer on pytest fixtures - https://docs.pytest.org/en/6.2.x/fixture.html 

@pytest.fixture()
def setup():
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
    prefs["profile.default_content_settings.popups"]=0
    # getcwd should always return the root directory of the framework
    prefs["download.default_directory"]=f"{os.getcwd()}\\ActualOutputs"
    options.add_experimental_option("prefs", prefs)
    options.add_argument("window-size=1920,1080")
    # if ReadConfig.ifHeadlessMode() == 'yes':
    if ReadConfig.ifHeadlessMode().strip().lower() == 'yes':
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")  # fatal
    elif ReadConfig.ifHeadlessMode() == 'no':
        pass
    else:
        raise Exception("Only values - yes, no - are permitted for the ifHeadlessMode variable")
    options.add_experimental_option('excludeSwitches',['enable-logging'])

    # driver = webdriver.Chrome(options=options,executable_path=f"{os.getcwd()}\\utilities\\chromedriver")

    # driver=webdriver.Chrome()
    driver = webdriver.Chrome(options=options) 

    #Edge browser setting
    # driver = webdriver.Edge(executable_path=f"{os.getcwd()}\\utilities\\msedgedriver")

    driver.maximize_window()
    driver.implicitly_wait(15)
    # added this part to automatically quit driver once the test is completed
    yield driver
    driver.quit()

############## pytest HTML Report ##############
# @pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # config._metadata['Test Suite'] = ReadConfig.getwrapperTestData().replace(".xlsx","")
    config._metadata['Machine Configuration'] = f'{socket.getfqdn()}, {platform.processor()}, {str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"}'
    config._metadata['Application URL'] = ReadConfig.getApplicationURL()
    config._metadata['Tester'] = ReadConfig.getUserName()
    config._metadata['OS'] = platform.platform()
    config._metadata['Browser'] = 'Chrome'
 
    # set custom options only if none are provided from command line
    # create report target dir
    reports_dir = Path('Reports')
    reports_dir.mkdir(parents=True, exist_ok=True)
    # custom report file
    report = reports_dir / f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.html"
    # adjust plugin options
    config.option.htmlpath = report
    
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)
    metadata.pop("Packages",None)
    metadata.pop("Platform",None)
    metadata.pop("Python",None)

def pytest_html_report_title(report):
    ''' modifying the title  of html report'''
    report.title = "Automation Report"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(report, "duration_formatter", "%M:%S")
    report._title = getattr(item, '_title', '')
    report._tcid = getattr(item, '_tcid', '')
    report._filepath = getattr(item,'_filepath','')

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    del cells[1]
    cells.insert(1,html.th('TC ID'))
    cells.insert(2,html.th('Title'))
    cells.insert(3,html.th('Data file path'))
    cells.pop()

# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
#     del cells[1]
#     cells.insert(1,html.td(report._tcid))
#     cells.insert(2, html.td(report._title))
#     cells.insert(3,html.td(report._filepath))
#     cells.pop()

# # This deletes the log window in the report
# def pytest_html_results_table_html(data):
#         del data[-1]

# @pytest.hookimpl(trylast=True)
# def pytest_sessionfinish():
#     stat = tr.update_testrail()
#     print(stat)

# @pytest.hookimpl(trylast=True)
# def pytest_sessionfinish(session, exitstatus):

#     # Converting the HTML report file to PDF format
#     filename = Path(glob.glob('Reports//*.html')[0]).stem
#     path = os.path.abspath(f'Reports//{filename}.html')
#     converter.convert(f'file:///{path}?collapsed=Skipped', f"{filename}.pdf")

#     # Modifying the xml file for testrail result upload
#     doc = xml.dom.minidom.parse(f'Reports/junit-results.xml')

#     for tc in doc.getElementsByTagName('testcase'):

#         properties = doc.createElement('properties')
#         tc.appendChild(properties)

#         # Adding the properties tag to attach the evidences
#         property1 = doc.createElement('property')
#         property1.setAttribute('name', 'testrail_attachment')
#         property1.setAttribute('value', f"{filename}.pdf")
#         properties.appendChild(property1)

#         # Adding the properties tag to add the comment
#         property2 = doc.createElement('property')
#         property2.setAttribute('name', 'testrail_result_comment')
#         property2.setAttribute('value', "Pytest Automated Test Results")
#         properties.appendChild(property2)

#         # When Testcase is failed then an extra properties tag will be added to upload the exception details to
#         # know in which step exactly the test case if failed.
#         index = 1
#         for child in tc.childNodes:
#             if child.nodeName == 'failure':
#                 for xy in doc.getElementsByTagName('failure'):
#                     if xy.attributes['message'].value != "**Test is Failed**":
#                         text = xy.childNodes[0].nodeValue
#                         dirpath = os.getcwd()
#                         isExist = os.path.exists(dirpath)
#                         if isExist:
#                             filepath = Path(os.getcwd() + f"\\exception_file_{index}.txt")
#                             filepath.touch(exist_ok=True)
#                         elif not isExist:
#                             os.makedirs(dirpath)
#                             filepath = Path(os.getcwd() + f"\\exception_file_{index}.txt")
#                             filepath.touch(exist_ok=True)

#                         file = open(f'exception_file_{index}.txt', 'w')
#                         file.write(text)
#                         file.close()

#                         property3 = doc.createElement('property')
#                         property3.setAttribute('name', 'testrail_attachment')
#                         property3.setAttribute('value', f'exception_file_{index}.txt')
#                         properties.appendChild(property3)

#                         xy.attributes['message'].value = "**Test is Failed**"
#                         xy.childNodes[0].nodeValue = f"Actual results does not meet with Expected results. Hence " \
#                                                      f"the test case is failed. Please find the attached exception " \
#                                                      f"results 'exception_file_{index}.txt' file for more information."
#                         break
#                     index += 1

#     xml_str = doc.toprettyxml(indent="\t")
#     save_path_file = f"Reports/junit-results.xml"
#     save_path_file1 = f"junit-results.xml"

#     with open(save_path_file, "w") as f:
#         f.write(xml_str)
#     with open(save_path_file1, "w") as f:
#         f.write(xml_str)
