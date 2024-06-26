import os
import time
from Helpers.Base import Base 
from Helpers.ExcelHelper import Excel_HelperFunctions
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from Helpers.NewInputHelper import NewInputHelper
from selenium.webdriver.common.by import By
from Helpers.Ad_Design_Helper import AD_DesignPageHelperfunctions
# import pyautogui

class Sim_Result_Helperfunctions:
    
    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)
        self.functionsforexcel = Excel_HelperFunctions(self.driver, extra)
        self.newinputcreation = NewInputHelper(self.driver,extra)
        self.ResultHelpers=AD_DesignPageHelperfunctions(self.driver,extra)
    
    def validate_sim_results(self, datafile, row_data, LogScreenshot, tc_status):
        """
        Validate the results page against the expected values from the datafile.

        Parameters:
            datafile (pd.DataFrame): DataFrame containing test data.
            row_data (pd.Series): Series containing row data from datafile DataFrame.
            LogScreenshot (cLogScreenshot): LogScreenshot instance for logging and capturing screenshots.
            tc_status (list): List to store test case status ('PASS' or 'FAIL').
        """
        try:
            
            # Retrieve actual results from the results page
            actual_results = self.get_actual_sim_results()

            # Compare actual results with expected values (row_data)
            matching_columns = []
            mismatching_columns = []

            for column, expected_value in row_data.items():
                actual_value = actual_results.get(column, None)
                
                if actual_value is not None and actual_value != 'N/A' and expected_value != 'nan':
                    result = self.ResultHelpers.assert_passforSciChars(expected_value, actual_value)
                    print(result)
                    if self.ResultHelpers.check_if_is_number(actual_value) and self.ResultHelpers.check_if_is_number(expected_value):
                        actual_value = round(float(actual_value), 3)
                        expected_value = round(float(expected_value), 3)
                    else:
                        actual_value = str(actual_value)
                        expected_value = str(expected_value)

                    if str(actual_value) == str(expected_value) or result == "PASS":
                        matching_columns.append((column, expected_value, actual_value))
                        tc_status.append("PASS")
                    else:
                        mismatching_columns.append((column, expected_value, actual_value))
                        tc_status.append("FAIL")

            self.LogScreenshot.fLogScreenshot(message=f"Results page", pass_=True, log=True, screenshot=True)
            time.sleep(2)  # Wait for 1 second to load new content 
            
            # self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div[3]')
            # time.sleep(2)  # Wait for 1 second to load new content 
            # self.LogScreenshot.fLogScreenshot(message=f"Results page - Part 2", pass_=True, log=True, screenshot=True)

            # Log mismatching columns and their values
            if matching_columns:
                for column, expected, actual in matching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Matching column '{column}': Expected({expected}), Actual({actual})",                                                
                                            pass_=True, log=True, screenshot=False)
            
            # Log mismatching columns and their values
            if mismatching_columns:
                for column, expected, actual in mismatching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Mismatching column '{column}': Expected({expected}), Actual({actual})",
                                                pass_=False, log=True, screenshot=False)            

        except Exception as e:
            LogScreenshot.fLogScreenshot(
                message=f"Error in results validation: {e}",
                pass_=False, log=True, screenshot=True
            )
            tc_status.append("FAIL")

    def get_actual_sim_results(self):
        """
        Retrieve actual results from the results page and return as a dictionary.

        This method should be customized based on how actual results are extracted from your application's UI.

        Returns:
            dict: Dictionary containing actual results (column names mapped to their values).
        """
        actual_results = {}       
        try:
            # Assuming your provided code snippet correctly extracts key-value pairs from the webpage
            key_elements = self.base.findElements("Keyxpath")
            time.sleep(5)
            value_elements = self.base.findElements("Valuexpath")
            time.sleep(5)
            Webpage_dict = self.functionsforexcel.getalltheKeyValuepairofPage(Key_xpath=key_elements, Value_Xpath=value_elements)
            self.LogScreenshot.fLogScreenshot(message=f"Extracted key value pairs with Results page",
                                            pass_=True, log=True, screenshot=True)
            # Assign specific key-value pairs based on column_to_key_mapping
            actual_results['StudyObjective'] = Webpage_dict.get('Study Objective', 'N/A')
            actual_results['Phase'] = Webpage_dict.get('Phase', 'N/A')
            actual_results['TargetPopulation'] = Webpage_dict.get('Target Population', 'N/A')
            actual_results['ControlArm'] = Webpage_dict.get('Control Arm', 'N/A')
            actual_results['TreatmentArm'] = Webpage_dict.get('Treatment Arm', 'N/A')
            actual_results['Priority'] = Webpage_dict.get('Priority', 'N/A')
            actual_results['EndpointName'] = Webpage_dict.get('Endpoint Name', 'N/A')
            actual_results['EndpointType'] = Webpage_dict.get('Endpoint Type', 'N/A')
            actual_results['BetterResponse'] = Webpage_dict.get('Better Response', 'N/A')
            actual_results['FollowUpTime'] = Webpage_dict.get('Follow-up Time', 'N/A')
            actual_results['StatisticalDesign'] = Webpage_dict.get('StatisticalDesign', 'N/A')
            actual_results['Test'] = Webpage_dict.get('Test', 'N/A')
            actual_results['Hypothesis'] = Webpage_dict.get('Hypothesis', 'N/A')
            actual_results['TestType'] = Webpage_dict.get('Test Type', 'N/A')
            actual_results['simInput_allocationRatio'] = Webpage_dict.get('Allocation Ratio', 'N/A')
            actual_results['simInput_testStatistic'] = Webpage_dict.get('Test Statistic', 'N/A')
            actual_results['simInput_meanCtrl'] = Webpage_dict.get('Mean Control', 'N/A')
            actual_results['simInput_meanTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')
            actual_results['simInput_stdDeviation'] = Webpage_dict.get('Standard Deviation', 'N/A')
            actual_results['simInput_sampleSize'] = Webpage_dict.get('Sample Size', 'N/A')            
            actual_results['simInput_probOfDropout'] = Webpage_dict.get('', 'N/A')
            actual_results['simInput_varianceType'] = Webpage_dict.get('', 'N/A')        
            actual_results['simInput_criticalPt'] = Webpage_dict.get('', 'N/A')
            actual_results['simInput_dataGenUsing'] = Webpage_dict.get('Input Method', 'N/A')
            actual_results['simInput_method'] = Webpage_dict.get('Randomization Method', 'N/A')
            actual_results['simInput_stdDeviationCtrl'] = Webpage_dict.get('SD Control', 'N/A')
            actual_results['simInput_stdDeviationTrmt'] = Webpage_dict.get('SD Treatment', 'N/A')
            actual_results['simInput_numOfSims'] = Webpage_dict.get('Number of Simulations Run', 'N/A')
            actual_results['Sim_RanNumSeed'] = Webpage_dict.get('Random Number Seed', 'N/A')
            actual_results['simInput_margin'] = Webpage_dict.get('Noninferiority Margin', 'N/A')
            actual_results['simInput_distofAccrualTime'] = Webpage_dict.get('Accrual Model', 'N/A')
            actual_results['simInput_margin'] = Webpage_dict.get('Super Superiority Margin', 'N/A')
            actual_results['simInput_propResponseUnderAlt'] = Webpage_dict.get('Proportion Response', 'N/A')
            actual_results['siminput_propResponseUnderNull'] = Webpage_dict.get('Proportion Response under Null', 'N/A')
            
            #output fields
            actual_results['simOut_totSimsPerAnlys'] = Webpage_dict.get('Starting Seed', 'N/A')
            actual_results['simOut_totSuccessSims'] = Webpage_dict.get('Total Number of Simulations', 'N/A')            

        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error while extracting actual results: {e}",
                                            pass_=False, log=True, screenshot=True)
        return actual_results
    
    def Analyticalvalidate_results(self, datafile, row_data, LogScreenshot, tc_status):
        """
        Validate the results page against the expected values from the datafile.

        Parameters:
            datafile (pd.DataFrame): DataFrame containing test data.
            row_data (pd.Series): Series containing row data from datafile DataFrame.
            LogScreenshot (cLogScreenshot): LogScreenshot instance for logging and capturing screenshots.
            tc_status (list): List to store test case status ('PASS' or 'FAIL').
        """
        
        # Retrieve actual results from the results page
        actual_results = self.Analytical_get_actual_results_from_page()

        # Compare actual results with expected values (row_data)
        matching_columns = []
        mismatching_columns = []

        for column, expected_value in row_data.items():
            actual_value = actual_results.get(column, None)
            if actual_value is not None:
                if str(actual_value) == str(expected_value):
                    matching_columns.append(column)
                    tc_status.append("PASS")
                else:
                    mismatching_columns.append((column, expected_value, actual_value))
                    tc_status.append("FAIL")

        # Log matching columns
        if matching_columns:
            # for column, expected, actual in matching_columns:
            #     LogScreenshot.fLogScreenshot(message=f"Matching Columns '{column}': Expected({expected}), Actual({actual})",
            #                                 pass_=False, log=True, screenshot=True)
                LogScreenshot.fLogScreenshot(message=f"Matching Columns: {', '.join(matching_columns)}",
                                        pass_=True, log=True, screenshot=True)
        # print("Matching Columns: ", column, expected, actual, "\n ")
        # Log mismatching columns and their values
        if mismatching_columns:
            for column, expected, actual in mismatching_columns:
                LogScreenshot.fLogScreenshot(message=f"Mismatching column '{column}': Expected({expected}), Actual({actual})",
                                            pass_=False, log=True, screenshot=True)
        print("MisMatching Columns: ", column, expected, actual, "\n ")
        tc_status.append("FAIL")

    def Analytical_get_actual_results_from_page(self):
        """
        Retrieve actual results from the results page and return as a dictionary.

        This method should be customized based on how actual results are extracted from your application's UI.

        Returns:
            dict: Dictionary containing actual results (column names mapped to their values).
        """
        actual_results = {}

        # Example: Extract actual results from the results page and populate actual_results dictionary
        # Modify this section to match how results are retrieved in your application
        # Add more entries for other columns...
        column_to_key_mapping = {
        # Excel key: WebPage Key
        'StudyObjective': 'Study Objective',
        'Phase': 'Phase',
        'TargetPopulation': 'TargetPopulation',
        'ControlArm': 'Control Arm',
        'TreatmentArm': 'Treatment Arm',
        'Priority': 'Priority',
        'EndpointName': 'Endpoint Name',
        'EndpointType': 'Endpoint Type',
        'BetterResponse': 'Better Response',
        'FollowUpTime': 'Follow-up Time',
        'DesignType': 'Hypothesis',
        'A_Interims' :'Interims',
        'TestType':'Test Type',
        'AD_sampleSize': 'Sample Size',
        'TestType' : 'Designs.Test Type',
        'simInput_sampleSize': 'Sample Size',
        'simInput_testStatistic': 'Designs.Test Statistic',
        'simInput_margin': 'Designs.Noninferiority Margin / Designs.Noninferiority Margin',
        'simInput_stdDeviation': 'Std. Deviation',
        'simInput_varianceType': 'Designs.Variance',
        'simInput_dataGenUsing': 'Responses.Input Method',
        'simInput_meanCtrl': 'Mean Control',
        'simInput_meanTrmt': 'Mean Treatment',
        'simInput_stdDeviationCtrl': 'SD Control',
        'simInput_stdDeviationTrmt': 'SD Treatment',
        'simInput_numOfSims': 'Number of Simulations Run',
        'simInput_seedVal': 'Starting Seed',
        'simInput_distofAccrualTime': 'Accrual Model',
        'simInput_numAccrualPeriods': 'Period',
        'simInput_startTime': 'Starting aAt Time',
        'simInput_accrualRate': 'Avg. Subjects Enrolled',
        'simInput_responseLag': 'Follow-up Time',
        'simInput_probOfDropout': 'Probability of Dropout',
        'simInput_method': 'Designs.Randomization Method',
        'simInput_criticalPtLwr': 'Interim.IA1.Boundaries.Lower Efficacy',
        'simInput_criticalPtUpr': 'Interim.IA1.Boundaries.Upper Efficacy',
        'simInput_criticalPt': 'Interim.IA1.Boundaries.Efficacy',
        'simInput_allocationRatio': 'Designs.Allocation Ratio',
        'simOut_accrualDuration': 'Total Accrual Duration',
        'simOut_avgLookTimePerAnlys': 'Interim.IA1.Average Look Time',
        'simOut_avgLookTime': 'Interim.Average.Average Look Time',
        'simOut_avgPipelinePerAnlys': 'Interim.IA1.Average Pipeline',
        'simOut_avgPipeline': 'Interim.Average.Average Pipeline',
        'simOut_avgSampleSizePerAnlys': 'Interim.IA1.Average Sample Size',
        'simOut_avgSampleSize': 'Interim.Average.Average Sample Size',
        'simOut_avgCompletersPerAnlys': 'Interim.IA1.Average Completers',
        'simOut_avgCompleters': 'Interim.Average.Average Completers',
        'simOut_avgDropoutsPerAnlys': 'Interim.IA1.Average Dropouts',
        'simOut_avgDropouts': 'Interim.Average.Average Dropouts',
        'simOut_completersPerAnlys': 'Interim.IA1.Completers',
        'simOut_avgPowerAtTermination': 'Designs.Avg. Power at Termination',
        'simOut_avgPowerAtFA': 'Designs.Avg. Power at Final Analysis',
        'simOut_stopForEffPerAnlys': 'Interim.IA1.Stopping For.Efficacy',
        'simOut_totEffCnt': 'Interim.Total.Stopping For.Efficacy',
        'simOut_stopForEffTotalPerc': 'Interim.%.Stopping For.Efficacy',
        'simOut_stopForUprEffPerAnlys': 'Interim.IA1.Stopping For.Upper Efficacy',
        'simOut_totUprEffCnt': 'Interim.Total.Stopping For.Upper Efficacy',
        'simOut_stopForUprEffTotalPerc': 'Interim.%.Stopping For.Upper Efficacy',
        'simOut_stopForLwrEffPerAnlys': 'Interim.IA1.Stopping For.Lower Efficacy',
        'simOut_totLwrEffCnt': 'Interim.Total.Stopping For.Lower Efficacy',
        'simOut_stopForLwrEffTotalPerc': 'Interim.%.Stopping For.Lower Efficacy',
        'simOut_totSimsPerAnlys': 'Interim.IA1.Count',
        'simOut_totSimsPercPerAnlys': 'Interim.IA1.%',
        'simOut_totSuccessSims': 'Interim.Total.Count'

        }

        """
        Retrieve actual results from the results page and return as a dictionary.

        This method should be customized based on how actual results are extracted from your application's UI.

        Returns:
            dict: Dictionary containing actual results (column names mapped to their values).
        """
        actual_results = {}
        try:
            # Assuming your provided code snippet correctly extracts key-value pairs from the webpage
            key_elements = self.base.findElements("Keyxpath")
            time.sleep(5)
            value_elements = self.base.findElements("Valuexpath")
            time.sleep(5)
            Webpage_dict = self.functionsforexcel.getalltheKeyValuepairofPage(Key_xpath=key_elements, Value_Xpath=value_elements)
            self.LogScreenshot.fLogScreenshot(message=f"Extracted key value pairs with Results page",
                                            pass_=True, log=True, screenshot=True)

            print("webpage dict : ", Webpage_dict)
            # # Assign the extracted key-value pairs to the actual_results dictionary
            # for key, value in Webpage_dict.items():
            #     actual_results[key] = value

            # Assign specific key-value pairs based on column_to_key_mapping
            actual_results['StudyObjective'] = Webpage_dict.get('Study Objective', 'N/A')
            actual_results['Phase'] = Webpage_dict.get('Phase', 'N/A')
            actual_results['TargetPopulation'] = Webpage_dict.get('Target Population', 'N/A')
            actual_results['ControlArm'] = Webpage_dict.get('Control Arm', 'N/A')
            actual_results['TreatmentArm'] = Webpage_dict.get('Treatment Arm', 'N/A')
            actual_results['Priority'] = Webpage_dict.get('Priority', 'N/A')
            actual_results['EndpointName'] = Webpage_dict.get('Endpoint Name', 'N/A')
            actual_results['EndpointType'] = Webpage_dict.get('Endpoint Type', 'N/A')
            actual_results['BetterResponse'] = Webpage_dict.get('Better Response', 'N/A')
            actual_results['FollowUpTime'] = Webpage_dict.get('Follow-up Time', 'N/A')
            actual_results['A_Interims'] = Webpage_dict.get('Interims', 'N/A')
            actual_results['Variance'] = Webpage_dict.get('Test', 'N/A')
            actual_results['Test Statistic'] = Webpage_dict.get('Input Method', 'N/A')
            # actual_results['AD_AvgPowerTermination'] = Webpage_dict.get('Avg. Power at Termination', 'N/A')
            # actual_results['TestType'] = Webpage_dict.get('Test Type', 'N/A')
            # actual_results['TypeIError'] = Webpage_dict.get('Type 1 Error', 'N/A')
            actual_results['AD_sampleSize'] = Webpage_dict.get('Sample Size', 'N/A')
            # actual_results['input_typeIError'] = Webpage_dict.get('Type 1 Error', 'N/A')
            # actual_results['input_power'] = Webpage_dict.get('Power', 'N/A')
            # actual_results['AllocationRatio'] = Webpage_dict.get('Allocation Ratio', 'N/A')
            # actual_results['TestStatistic'] = Webpage_dict.get('Test Statistic', 'N/A')
            # actual_results['meanCtrl'] = Webpage_dict.get('Mean Control', 'N/A')
            # actual_results['meanTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')
            # actual_results['stdDeviation'] = Webpage_dict.get('Standard Deviation', 'N/A')
            # actual_results['sampleSize'] = Webpage_dict.get('Sample Size', 'N/A')
            # actual_results['sampleSizeCtrl'] = Webpage_dict.get('Control', 'N/A')
            # actual_results['sampleSizeTrmt'] = Webpage_dict.get('Treatment', 'N/A')
            # actual_results['power'] = Webpage_dict.get('Power', 'N/A')
            # actual_results['probofSuccess'] = Webpage_dict.get('Probability of Success', 'N/A')
            # actual_results['Variance'] = Webpage_dict.get('Variance', 'N/A')
            # actual_results['distribution'] = Webpage_dict.get('Prior Distribution for', 'N/A')
            # actual_results['Assurance_InputMethod'] = Webpage_dict.get('Input Method', 'N/A')
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error while extracting actual results: {e}",
                                            pass_=False, log=True, screenshot=True)
        return actual_results
    
    