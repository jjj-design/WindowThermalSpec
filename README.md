# 開口部の評価方法に関する仕様書

## 計算ファイルの依存関係整理
(<--:引用、-->:被引用)  

### K系プログラム

* jjj_shg_spec(main)  
<-- WEA  
<-- SP  
<-- SG2BDR  
<-- SROTS  
<-- oblique_incidence_property  
<-- glass_thermal_balance  
<-- TU  
<-- ISROG  
<-- TSRTG  
<-- ASRIG  
<-- SHTFG  
<-- HGOG  

* division_diffuse_ratio  
--> TSRTG  
--> ASRIG   
<-- None  

* glass_thermal_balance  
--> main  

* multiple_reflection  
--> TSRTG  
--> ASRIG  
<-- None  

* oblique_incidence_property  
--> TSRTG  
--> ASRIG  
--> main  
<-- None  

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

* SplittingGlobal2BeamDiffuseRadiation(SG2BDR)  
--> main  
<-- WEA(only in Example)  
<-- SP(only in Example)  

* SolarRadiationOnTiltedSurface(SROTS)  
--> main  
<-- WEA(only in Example)  

* TransformUnit(TU)  
--> main  
<-- None  

* IncidentSolarRadiationOnGlazing(ISROG)  
--> TSRTG(only in Example)  
--> ASRIG(only in Example)  
--> main  
<-- None  

* TransmittedSolarRadiationThroughGlazing(TSRTG)  
<-- oblique_incidence_property  
<-- multiple_reflection  
<-- division_diffuse_ratio  
<-- ISROG(only in Example)  
--> main  

* AbsorbedSolarRadiationIntoGlazing(ASRIG)  
<-- oblique_incidence_property  
<-- multiple_reflection  
<-- division_diffuse_ratio  
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
