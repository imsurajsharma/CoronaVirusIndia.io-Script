from django.shortcuts import render
import requests
from django.http import JsonResponse

# Create your views here.

def dashboard(request):
    
    if request.method == "POST":
        pass
        # districtAPI= "https://api.covid19india.org/state_district_wise.json"
        # districtRespond= requests.get(districtAPI)
        # distRes=districtRespond.json()

        # print(distRes)
    
    else:
        districtAPI= "https://api.covid19india.org/state_district_wise.json"
        districtRespond= requests.get(districtAPI)
        distRes=districtRespond.json()

        for key in distRes:
            print(key, "->" , distRes[key])

      

        

        distList=list()
        

        # for state in range(0,len(distRes)):
        #     dist=distRes[state]
        #     print(dist)

        
        return render(request,"dash.html")

def index(request):

    if request.method=="POST":
        api='https://api.rootnet.in/covid19-in/stats/latest'
        dailyAPI= 'https://api.rootnet.in/covid19-in/stats/daily'
        testAPI="https://api.rootnet.in/covid19-in/stats/testing/latest"
        unofficialAPI="https://v1.api.covindia.com/general"

        respond=requests.get(api)
        res=respond.json()

        dailyRespond=requests.get(dailyAPI)
        dailyRes=dailyRespond.json()

        testRespond =requests.get(testAPI)
        testRes =testRespond.json()

        
        unRespond =requests.get(unofficialAPI)
        unRes = unRespond.json()
        unOffDeath=unRes["deathTotal"]
        unOffRec = unRes["totalCured"]
        unOffConf =unRes["infectedTotal"]
        unOffAct = unOffConf - unOffRec -unOffDeath

        unOffSummary = {"unOffConf":unOffConf,"unOffAct":unOffAct,"unOffRec":unOffRec,"unOffDeath":unOffDeath}
       
        # summary data
        totalConfirm=res["data"]["summary"]["total"]
        totalDeath=res["data"]["summary"]["deaths"]
        totalRecover=res["data"]["summary"]["discharged"]

        summary = {'totalConfirm':totalConfirm,"totalDeath":totalDeath,"totalRecover":totalRecover}

        # daily stats
        dailyConfirmList=list()
        dailyDeathList=list()
        dailyRecoverList=list()
        dailyActiveList=list()
        # daily stats end


        state_name= list()
        confirmedList= list()
        activeList=list()
        recoverList=list()
        deathList=list()
        states= list()
        num=len(res["data"]["regional"])
        for i in range(0,len(res["data"]["regional"])):
            caseIndia= res["data"]["regional"][i]["confirmedCasesIndian"]
            caseForeign=res["data"]["regional"][i]["confirmedCasesForeign"]
            confirmedCase=caseIndia+caseForeign
            confirmedList.append(confirmedCase)
            recoverCase=res["data"]["regional"][i]["discharged"]
            recoverList.append(recoverCase)
            deathCase = res["data"]["regional"][i]["deaths"]
            deathList.append(deathCase)
            activeCase=confirmedCase-recoverCase -deathCase
            activeList.append(activeCase)
            ap = res["data"]["regional"][i]["confirmedCasesIndian"] + caseForeign
            nm = res["data"]["regional"][i]["loc"]
            state_name.append(nm)
            states.append(ap)

        for d in range(0,len(dailyRes["data"])):
            
            # dailyRes stats loop
            dailyCase=dailyRes["data"][d]["summary"]["total"]
            dailyRecover=dailyRes["data"][d]["summary"]["discharged"]
            dailyDeath=dailyRes["data"][d]["summary"]["deaths"]
            dailyActive= dailyCase - (dailyRecover + dailyDeath)

            dailyConfirmList.append(dailyCase)
            dailyDeathList.append(dailyDeath)
            dailyRecoverList.append(dailyRecover)
            dailyActiveList.append(dailyActive)

        testDay= testRes["data"]["day"]
        testSample=testRes["data"]["totalSamplesTested"]
        testIndividual=testRes["data"]["totalIndividualsTested"]
        testPositive=testRes["data"]["totalPositiveCases"]
        testSource = testRes["data"]["source"]
        testUpdate=testRes["lastOriginUpdate"]

        testSummary={"testDay":testDay,"testSample":testSample,"testIndividual":testIndividual,"testPositive":testPositive,"testSource":testSource,"testUpdate":testUpdate}


        #daily stats for states
        # lastStateName= dailyRes["data"][-1]

        # lastStateList = list()
        # lastConfirmList = list()
        # lastDeathList = list()
        # lastRecList = list()

        # for last in range(0,len(dailyRes["data"][-1]["regional"])):

        #     lastStates=dailyRes["data"][-1]["regional"][last]["loc"] 
        #     lastConfirmCaseIndia= dailyRes["data"][-1]["regional"][last]["confirmedCasesIndian"] 
        #     lastConfirmCaseForeign =dailyRes["data"][-1]["regional"][last]["confirmedCasesForeign"]
        #     lastConfirmCase = lastConfirmCaseIndia + lastConfirmCaseForeign
        #     lastDeath=dailyRes["data"][-1]["regional"][last]["deaths"]
        #     lastRecover=dailyRes["data"][-1]["regional"][last]["discharged"]

        #     lastStateList.append(lastStates)
        #     lastConfirmList.append(lastConfirmCase)
        #     lastDeathList.append(lastDeath)
        #     lastRecList.append(lastRecover)

        # lastSummary={"lastStateList":lastStateList,"lastConfirmList":lastConfirmList,"lastDeathList":lastDeathList,"lastRecList":lastRecList}

            
        dailySummary={"dailyConfirmed":dailyConfirmList,"dailyDeath":dailyDeathList,"dailyRecover":dailyRecoverList,"dailyActiveList":dailyActiveList}
        
     

        gdata=dict(zip(state_name,states))

    
    

        return JsonResponse({'graph':gdata,'stateName':state_name,"confirmedCase":confirmedList,"active":activeList,"recover":recoverList,"death":deathList,"num":num,"summary":summary,"dsum":dailySummary,"testSummary":testSummary,"unOffSummary":unOffSummary}, safe=False)
    else:
        return render(request,"index.html")


def whyUs(request):
    return render(request,"why.html")

def aboutUs(request):
    return render(request,"about.html")

def contactUs(request):
    return render(request,"contact.html")