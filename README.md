# 開口部の評価方法に関する仕様書

## 計算ファイルの依存関係整理
(<--:引用、-->:被引用)  

* jjj_shg_spec(main)  
<-- WEA  
<-- SP  
<-- SG2BDR  
<-- SROTS  
<-- GAP  
<-- RAP  
<-- HB  
<-- TU  
<-- ISROG  
<-- TSRTG  
<-- ASRIG  
<-- SHTFG  
<-- HGOG  


* Weather(WEA)  
--> HCP(only in Example)  
--> SP(only in Example)  
--> SG2BDR(only in Example)  
--> SROTS(only in Example)  
--> main  
<-- None  

* HeatingCoolingPeriod(HCP)  
--> None  
<-- WEA(only in Example)  

* SolarPosition(SP)  
--> SG2BDR(only in Example)  
--> main  
<-- WEA(only in Example)  

* DivisionDiffuseRatio(DDR)  
--> TSRTG  
--> ASRIG   
<-- None  

* SplittingGlobal2BeamDiffuseRadiation(SG2BDR)  
--> main  
<-- WEA(only in Example)  
<-- SP(only in Example)  

* SolarRadiationOnTiltedSurface(SROTS)  
--> main  
<-- WEA(only in Example)  

* GlassAngularProperty(GAP)  
--> TSRTG  
--> ASRIG  
--> main
<-- None  

* RollershadeAngularProperty(RAP)  
--> TSRTG  
--> ASRIG  
--> main  
<-- None  

* MultipleReflectionOfSolarRadiation(MROSR)  
--> TSRTG  
--> ASRIG  
<-- None  

* PaneResistance(PR)  
--> HB  
<-- None  

* ClosedCavityResistance(CCR)  
--> HB  
<-- None  

* SurfaceResistance(SR)  
--> HB  
<-- None  

* HeatBalance(HB)  
--> main  
<-- PR  
<-- CCR  
<-- SR  

* TransformUnit(TU)  
--> main  
<-- None  

* IncidentSolarRadiationOnGlazing(ISROG)  
--> TSRTG(only in Example)  
--> ASRIG(only in Example)  
--> main  
<-- None  

* TransmittedSolarRadiationThroughGlazing(TSRTG)  
<-- GAP  
<-- RAP  
<-- MROSR  
<-- DDR  
<-- ISROG(only in Example)  
--> main  

* AbsorbedSolarRadiationIntoGlazing(ASRIG)  
<-- GAP  
<-- RAP  
<-- MROSR  
<-- DDR  
<-- ISROG(only in Example)  
--> main  

* SecondaryHeatTransferFromGlazing(SHTFG)  
<-- None  
--> main  

* HourlyGvalueOfGlazing(HGOG)  
<-- None  
--> main  

* HourlyGvalueOfFrame(HGOF)  
--> None  
<-- None  

* HourlyGvalueOfWindow(HGOW)  
--> None  
<-- None  