# 開口部の評価方法に関する仕様書

## 計算ファイルの依存関係整理
(<--:引用、-->:被引用)  

### K系プログラム

* jjj_shg_spec(main)  
<-- WEA  
<-- SP  
<-- SG2BDR  
<-- SROTS  
<-- GAP  
<-- RAP  
<-- glass_thermal_balance  
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
<-- sun_position

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

* multiple_reflection  
--> TSRTG  
--> ASRIG  
<-- None  

* glass_thermal_balance  
--> main  

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
<-- multiple_reflection  
<-- DDR  
<-- ISROG(only in Example)  
--> main  

* AbsorbedSolarRadiationIntoGlazing(ASRIG)  
<-- GAP  
<-- RAP  
<-- multiple_reflection  
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

### N系プログラム

* climate
<-- sun_position
--> Shading_Correction_Factor_Calculation
--> shading_effect_factor

* direct_solar_area
--> Shading_Correction_Factor_Calculation

* effect_coefficient
--> Shading_Correction_Factor_Calculation

* Shading_Correction_Factor_Calculation
<-- Shading_Correction_Factor_Main

* Shading_Correction_Factor_Main
<-- climate
<-- effect_coefficient
<-- sun_position
<-- direct_solar_area
<-- shading_effect_factor
--> Shading_Correction_Factor_Calculation

* shading_effect_factor
<-- climate
--> Shading_Correction_Factor_Main

### 共通モジュール

* sun_position
--> K系:SolarPosition(SP)
--> N系:climate
--> N系:Shading_Correction_Factor_Main
