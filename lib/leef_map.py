__author__ = 'Sacumen'

import json
import datetime

class LEEFJson:

    def __init__(
         self,
         severity,
         resourceId,
         alertRuleName,
         policyName,
         accountName,
         resourceName,
         riskRating,
         resourceRegion,
         policyDescription,
         policyRecommendation,

         resourceConfig,


         alertTs,
         callbackUrl,
         alertId,
         policyLabels,
         resourceType,
         hasFinding,
         resourceRegionId,

         source,
         cloudType,
         resourceCloudService

    ):
        self.severity = severity
        self.resourceId = resourceId
        self.alertRuleName = alertRuleName
        self.policyName = policyName
        self.accountName = accountName
        self.resourceName = resourceName
        self.riskRating = riskRating
        self.resourceRegion = resourceRegion
        self.policyDescription = policyDescription
        self.policyRecommendation = policyRecommendation

        self.resourceConfig = resourceConfig


        self.alertTs = alertTs
        self.callbackUrl = callbackUrl
        self.alertId = alertId
        self.policyLabels = policyLabels

        self.resourceType = resourceType

        self.hasFinding = hasFinding
        self.resourceRegionId = resourceRegionId

        self.source = source
        self.cloudType = cloudType
        self.resourceCloudService = resourceCloudService


    def __str__(self):
        l1 = []

       # l1.append("cat=" + 'redlocklog')
       # l1.append("eventID=" + 'redlock')
        l1.append("sev=" + str(self.severity))
        l1.append("resourceId=" + str(self.resourceId))
        l1.append("alertRuleName=" + str(self.alertRuleName))
        l1.append("policy=" + str(self.policyName))
        l1.append("accountName=" + str(self.accountName))
        l1.append("resource=" + str(self.resourceName))
        l1.append("riskRating=" + str(self.riskRating))
        l1.append("resourceRegion=" + str(self.resourceRegion))


        devTimeValue = datetime.datetime.utcfromtimestamp((self.alertTs)/ 1000.0).strftime('%b %d %Y  %H:%M:%S')

        l1.append("devTime="+ devTimeValue)

        l1.append("callbackUrl=" + str(self.callbackUrl))
        l1.append("alertId=" + str(self.alertId))

        polVal = json.dumps(self.policyLabels)
        polVal.replace("u'", "'")
        l1.append("policyLabels=" + polVal)


        l1.append("resourceType="+ str(self.resourceType))

        l1.append("hasFinding=" + str(self.hasFinding))
        l1.append("resourceRegionId=" + str(self.resourceRegionId))


        l1.append("source=" + str(self.source))
        l1.append("cloudType=" + str(self.cloudType))
        l1.append("resourceCloudService=" + str(self.resourceCloudService))

        str1 =  ' '.join(l1)

        return str1.strip()


def parseJson(jsonString):
    obj = json.loads(jsonString,strict=False)



    leefJsonObject =  LEEFJson(
        str(obj["severity"]),
        str(obj["resourceId"]),
        str(obj["alertRuleName"]),
        str(obj["policyName"]),
        str(obj["accountName"]),
        str(obj["resourceName"]),
        str(obj["riskRating"]),
        str(obj["resourceRegion"]),
        str(obj["policyDescription"]),
        str(obj["policyRecommendation"]),
        obj["resourceConfig"],

        int(obj["alertTs"]),
        str(obj["callbackUrl"]),
        str(obj["alertId"]),
        obj["policyLabels"],
        str(obj["resourceType"]),


        str(obj["hasFinding"]),
        str(obj["resourceRegionId"]),

        str(obj["source"]),
        str(obj["cloudType"]),
        str(obj["resourceCloudService"])

    )
    
    return leefJsonObject
