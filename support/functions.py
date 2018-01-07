__author__ = 'KHANH'
from database import DBSQL
from inadapter import IN
from ums import UMS
import datetime
from prettytable import PrettyTable
import time
import logging
import sys
import csv

logger = logging.getLogger(__name__)

THRESHOLD_DATA = 2500000 #20Mb - 2.5 MB
def yes_no():

    # raw_input returns the empty string for "enter"
    yes = set(['yes', 'y', 'ye'])

    choice = raw_input("Please respond with 'yes' or 'no':").lower()
    if choice in yes:
        return True
    else:
        return False


def check_quota_in_dn(dn):
    logger.info("Processing the number %s" % dn)
    example_db = DBSQL("example")
    try:
        example_db.connect()
        logger.debug("Open connection to DB successfully")
        example_in = IN("example")
        logger.info("Retrieving active plans...")
        result = []
        list_zero_quota = []
        logger.info("DateTime: %s" % str(datetime.datetime.now()))
        pretty_output = PrettyTable(["#", str(dn) + " PlanName",
                                     "PlanChargingPolicyUsageID",
                                     "BucketID", "Usage, Allocated, Quota", "IN Quota", "Status"])
        active_plans = example_db.get_active_plan(dn)
        i = 0
        if len(active_plans):  # more than 0 active plans
            buckets = example_in.get_usage(dn)
            if 'error' in buckets:  # print an error if fail in IN E///
                planname_err = pcpu_err = bucketid_err = uaq_err = inquota_err = status_err = 'IN_ERROR'
                pretty_output.add_row([i, planname_err, pcpu_err, bucketid_err, uaq_err, inquota_err, status_err])

            else:  # if no issue with getting bucket from IN E///
                for active_plan in active_plans:

                    # refine fields in sql query
                    active_plan_name = active_plan[0]
                    active_plan_pcpuid = active_plan[1]
                    active_plan_bucketid = int(active_plan[2])  # convert to int as its type is tring
                    active_plan_snid = active_plan[3]
                    for bucket in buckets:
                        if bucket['carrierServicePlanId']['bucketId'] == active_plan_bucketid:
                            i += 1
                            detail_active_plan = {'dn': dn,
                                                  'snid': active_plan_snid,
                                                  'bucketid': active_plan_bucketid,
                                                  'planname': active_plan_name,
                                                  'planpcpuid': active_plan_pcpuid,
                                                  'policytype': bucket['policyType'],
                                                  'inquota': bucket['quota']
                                                  }
                            pcpu_uaq = example_db.get_pcpu_uaq(detail_active_plan)
                            time.sleep(0.1)
                            status = "Unknown"
                            if pcpu_uaq is not None:
                                pcpu_usage = pcpu_uaq[0][0]
                                pcpu_allocated = pcpu_uaq[0][1]
                                pcpu_quota = pcpu_uaq[0][2]
                                # check if quota zero and pcpu_allocated not None
                                if bucket['quota'] == 0 \
                                        and pcpu_quota not in [None, 0] \
                                        and (pcpu_usage < pcpu_allocated
                                             or (pcpu_allocated in [None, 0] and pcpu_usage in [None, 0]) or (pcpu_allocated == pcpu_usage and pcpu_allocated < pcpu_quota)):
                                    list_zero_quota.append(detail_active_plan)
                                    status = "Mismatch"
                                elif pcpu_usage > pcpu_allocated and bucket['quota'] == 0 \
                                        and pcpu_quota not in [None, 0]:
                                    status = "Usage > Allocated"
                                elif pcpu_usage < 0 and pcpu_usage is not None and bucket['quota'] == 0 \
                                        and pcpu_quota not in [None, 0]:
                                    status = "Usage < 0"
                                #low data quota
                                elif 0 < bucket['quota'] < THRESHOLD_DATA and detail_active_plan['policytype'] == 'DATA' \
                                        and pcpu_quota not in [None, 0] \
                                        and (pcpu_usage < pcpu_allocated
                                             or (pcpu_allocated in [None, 0] and pcpu_usage in [None, 0])
                                             or (pcpu_allocated == pcpu_usage and pcpu_allocated < pcpu_quota)):

                                    list_zero_quota.append(detail_active_plan)
                                    status = "Low Quota"
                                    # status = "OK"
                                else:
                                    status = "OK"
                                uaq = str(pcpu_uaq)
                            else:
                                uaq = 'AN ERROR'
                            pretty_output.add_row([i, detail_active_plan['planname'],
                                                   detail_active_plan['planpcpuid'],
                                                   detail_active_plan['bucketid'],
                                                   uaq, detail_active_plan['inquota'], status])
                            detail_active_plan.update({'uaq': uaq, 'status': status})
                            result.append(detail_active_plan)
        logger.info(pretty_output)
        return {'active_plans': result, 'list_zero_quota': list_zero_quota}
    finally:
        example_db.close()
        logger.debug("Close connection to DB successfully")


def check_quota_in(list_number):
    logger.info("\n[*] CHECK USAGE")
    logger.info("Processing the list %s" % list_number)
    example_db = DBSQL("example")
    try:
        example_db.connect()
        logger.debug("Open connection to DB successfully")
        example_in = IN("example")
        logger.info("Retrieving active plans...")
        result = []
        list_zero_quota = []
        for dn in list_number:
            logger.info("")
            logger.info("DateTime: %s" % str(datetime.datetime.now()))
            pretty_output = PrettyTable(["#", str(dn) + " PlanName",
                                         "PlanChargingPolicyUsageID",
                                         "BucketID", "Usage, Allocated, Quota", "IN Quota", "Status"])
            active_plans = example_db.get_active_plan(dn)
            i = 0
            if len(active_plans):  # more than 0 active plans
                buckets = example_in.get_usage(dn)

                if 'error' in buckets:  # print an error if fail in IN E///
                    planname_err = pcpu_err = bucketid_err = uaq_err = inquota_err = status_err = 'IN_ERROR'
                    pretty_output.add_row([i, planname_err, pcpu_err, bucketid_err, uaq_err, inquota_err, status_err])

                else:  # if no issue with getting bucket from IN E///
                    for active_plan in active_plans:

                        # refine fields in sql query
                        active_plan_name = active_plan[0]
                        active_plan_pcpuid = active_plan[1]
                        active_plan_bucketid = int(active_plan[2])  # convert to int as its type is tring
                        active_plan_snid = active_plan[3]
                        for bucket in buckets:
                            if bucket['carrierServicePlanId']['bucketId'] == active_plan_bucketid:
                                i += 1
                                detail_active_plan = {'dn': dn,
                                                      'snid': active_plan_snid,
                                                      'bucketid': active_plan_bucketid,
                                                      'planname': active_plan_name,
                                                      'planpcpuid': active_plan_pcpuid,
                                                      'policytype': bucket['policyType'],
                                                      'inquota': bucket['quota']
                                                      }
                                pcpu_uaq = example_db.get_pcpu_uaq(detail_active_plan)
                                time.sleep(0.2)
                                status = "Unknown"
                                if pcpu_uaq is not None:
                                    pcpu_usage = pcpu_uaq[0][0]
                                    pcpu_allocated = pcpu_uaq[0][1]
                                    pcpu_quota = pcpu_uaq[0][2]
                                    # check if quota zero and pcpu_allocated not None
                                    if bucket['quota'] == 0 \
                                            and pcpu_quota not in [None, 0] \
                                            and (pcpu_usage < pcpu_allocated
                                                 or (pcpu_allocated in [None, 0] and pcpu_usage in [None, 0]) or (pcpu_allocated == pcpu_usage and pcpu_allocated < pcpu_quota)):
                                        list_zero_quota.append(detail_active_plan)
                                        status = "Mismatch"
                                    elif pcpu_usage > pcpu_allocated and bucket['quota'] == 0 \
                                            and pcpu_quota not in [None, 0]:
                                        status = "Usage > Allocated"
                                    elif pcpu_usage < 0 and pcpu_usage is not None and bucket['quota'] == 0 \
                                            and pcpu_quota not in [None, 0]:
                                        status = "Usage < 0"
                                    # low data quota
                                    elif 0 < bucket['quota'] < THRESHOLD_DATA and detail_active_plan['policytype'] == 'DATA' \
                                            and pcpu_quota not in [None, 0] \
                                            and (pcpu_usage < pcpu_allocated
                                                 or (pcpu_allocated in [None, 0] and pcpu_usage in [None, 0])
                                                 or (pcpu_allocated == pcpu_usage and pcpu_allocated < pcpu_quota)):

                                        list_zero_quota.append(detail_active_plan)
                                        status = "Low Quota"
                                        # status = "OK"
                                    else:
                                        status = "OK"
                                    uaq = str(pcpu_uaq)
                                else:
                                    uaq = 'AN ERROR'
                                pretty_output.add_row([i, detail_active_plan['planname'],
                                                       detail_active_plan['planpcpuid'],
                                                       detail_active_plan['bucketid'],
                                                       uaq, detail_active_plan['inquota'], status])
                                detail_active_plan.update({'uaq': uaq, 'status': status})
                                result.append(detail_active_plan)
            logger.info(pretty_output)
        return {'active_plans': result, 'list_zero_quota': list_zero_quota}
    finally:
        example_db.close()
        logger.debug("Close connection to DB successfully")


def check_quota_in_file(file):
    rf = open(file, 'rb')
    reader = csv.DictReader(rf)
    list_number = []
    for row in reader:
        if row['phonenumber'] not in list_number:
            list_number.append(row['phonenumber'])
    check_quota_in(list_number)

def sync_quota_in_dn(dn):
    logger.info("\n\n\n### SYNC QUOTA %s ###" % dn)
    logger.info("\n[*] CHECK USAGE")
    result_pre = check_quota_in_dn(dn)
    list_allocations = []  # list allocations
    list_zero_quota = result_pre['list_zero_quota']
    logger.debug("[*] List zero quota: %s" % list_zero_quota)
    logger.info("[*] Plans need to be processed:")

    if list_zero_quota:
        for entry in list_zero_quota:
            logger.info('planname: %s, planpcpuid: %s' % (entry['planname'], entry['planpcpuid']))
        try:

            logger.info("\n[*] UPDATE DATABASE:")
            example_db = DBSQL("example_write")
            example_db.connect()
            logger.debug("Open connection to DB successfully")
            list_ums_resync = []  # create at list of number, policytype for ums resync quota
            pretty_output = PrettyTable(["PhoneNumber", "PlanName", "PlanChargingPolicyUsageID",
                                         "BucketID", "Old Allocated", "New Allocated"])
            for entry in list_zero_quota:
                logger.info('planname: %s, planpcpuid: %s' % (entry['planname'], entry['planpcpuid']))
                logger.debug(entry)
                pair_ums = {'snid': entry['snid'], 'policytype': entry['policytype']}
                # add pair of snid, policytype for list ums resync
                if pair_ums not in list_ums_resync:
                    list_ums_resync.append(pair_ums)
                data = example_db.update_pcpu_sync(entry)
                pretty_output.add_row([entry['dn'], entry['planname'],
                                       entry['planpcpuid'], entry['bucketid'],
                                       data['original']['allocated'], data['new']['allocated']])

                if data['original']['allocated'] is None:
                    orginal_allocated = 0
                else:
                    orginal_allocated = int(data['original']['allocated'])

                if data['new']['allocated'] is None:
                    new_allocated = 0
                else:
                    new_allocated = int(data['new']['allocated'])
                list_allocations.append({'dn': entry['dn'], 'planname': entry['planname'],
                                         'bucketid': entry['bucketid'],
                                         'allocation': orginal_allocated - new_allocated})
                logger.info("")
            logger.debug("\n[*] UMS resync for list: %s" % list_ums_resync)
            example_ums = UMS("example")
            logger.info("[*] UMS Resync API:  Called")
            for element in list(list_ums_resync):
                example_ums.resync_usage(element['snid'], element['policytype'])
            logger.debug("\n\n### SUMMARY ###")
            logger.debug(pretty_output)

        finally:
            example_db.close()
            logger.debug("Close connection to DB successfully")
    else:
        logger.info(list_zero_quota)

    # recheck usage
    logger.info("\n[*] USAGE VERIFICATION")
    result_post = check_quota_in_dn(dn)
    return {'result_pre': result_pre, 'result_post': result_post, 'allocations': list_allocations}

def sync_quota_in(list_number):

    for dn in list_number:
        logger.info("\n\n\n### SYNC QUOTA %s ###" % dn)
        logger.info("\n[*] CHECK USAGE")
        result = check_quota_in_dn(dn)  # checking quota first
        list_zero_quota = result['list_zero_quota']
        logger.debug("[*] List zero quota: %s" % list_zero_quota)
        logger.info("[*] Plans need to be processed:")
        if list_zero_quota:
            #logger.info("!!! ATTENTION: continue?")
            #if yes_no():
                for entry in list_zero_quota:
                    logger.info('planname: %s, planpcpuid: %s' % (entry['planname'], entry['planpcpuid']))
                try:

                    logger.info("\n[*] UPDATE DATABASE:")
                    example_db = DBSQL("example_write")
                    example_db.connect()
                    logger.debug("Open connection to DB successfully")
                    list_ums_resync = []  # create at list of number, policytype for ums resync quota
                    pretty_output = PrettyTable(["PhoneNumber", "PlanName", "PlanChargingPolicyUsageID",
                                                 "BucketID", "Old Allocated", "New Allocated"])
                    for entry in list_zero_quota:
                        logger.info('planname: %s, planpcpuid: %s' % (entry['planname'], entry['planpcpuid']))
                        logger.debug(entry)
                        pair_ums = {'snid': entry['snid'], 'policytype': entry['policytype']}
                        # add pair of snid, policytype for list ums resync
                        if pair_ums not in list_ums_resync:
                            list_ums_resync.append(pair_ums)
                        data = example_db.update_pcpu_sync(entry)
                        pretty_output.add_row([entry['dn'], entry['planname'],
                                               entry['planpcpuid'], entry['bucketid'],
                                               data['original']['allocated'], data['new']['allocated']])
                        logger.info("")
                    logger.debug("\n[*] UMS resync for list: %s" % list_ums_resync)
                    example_ums = UMS("example")
                    logger.info("[*] UMS Resync API:  Called")
                    for element in list(list_ums_resync):
                        example_ums.resync_usage(element['snid'], element['policytype'])
                    logger.debug("\n\n### SUMMARY ###")
                    logger.debug(pretty_output)

                    #recheck usage
                    logger.info("\n[*] USAGE VERIFICATION")
                    check_quota_in_dn(dn)
                finally:
                    example_db.close()
                    logger.debug("Close connection to DB successfully")
            #else:
            #    logger.info("CANCELED...")
        else:
            logger.info(list_zero_quota)
    logger.info("\nFINISH")


def sync_quota_in_file(file):
    rf = open(file, 'rb')
    reader = csv.DictReader(rf)
    list_number = []
    for row in reader:
        if row['phonenumber'] not in list_number:
            list_number.append(row['phonenumber'])

    sync_quota_in(list_number)


