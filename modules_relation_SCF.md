# 開口部の評価方法に関する仕様書

## 計算ファイルの依存関係整理
(<--:引用、-->:被引用)  

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
<-- sun_position
--> Shading_Correction_Factor_Calculation

* sun_position
--> climate
--> Shading_Correction_Factor_Calculation
--> shading_effect_factor
