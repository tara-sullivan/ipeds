/******************************************************************************
File to clean raw ipeds data

Input: raw ipeds files; cip files created using ipeds_cip_merge.do

Output: ipeds_c_all.dta

Program defaults to running a panel of all data and saving that. It is possible 
to run a cross-section for a particular year using the command:

. do "`codepath'/ipeds_c_clean.do" 2018

This will save a version of the dataset called "`temppath'/ipeds_c_temp.csv".

This program creates a temporary file called temp, stores necessary datasets
created in ipeds_cip_merge.do, and then deletes the temp folder. It is possible
to turn off all of these features using globals/locals. 

Note to self: remember you can drop all macros using "macro drop _all"
******************************************************************************/
capture restore
set more off
set type double
clear all

local readdata 1
* note: might want to remove cipnames local;

if "`c(os)'" == "MacOSX" | "`c(os)'" == "Unix" {
	cd "/Users/tarasullivan/Documents/dissertation/data/ipeds/"
// 	local datapath "/Volumes/GoogleDrive/My Drive/data/IPEDS"
	local rawpath "/Volumes/GoogleDrive/My Drive/data/IPEDS"
}
else {
	cd "Z:\hcs"
}

// local datapath "ipeds/data"
local codepath "c/clean_data"
local temppath "c/clean_data/temp"
local savepath "c/clean_data"

* remove temporary directory at the end of code
global rm_temp_dir 1

* if a year arugumnt is passed, do not run as a cross section
if !missing("`1'") {
	if regexm("`1'", "[0-9][0-9][0-9][0-9]") {
		global panel_data = 0
		global cs_yr = `1'
		* save temporary version of the file
		local savetemp = 1
	}
}

* unless otherwise stated using a global, run program for panel
if strpos("${panel_data}", "0") {
	local savefile = 0
	if !missing("$cs_yr") {
		local startyr = $cs_yr
		local endyr = $cs_yr
	}
	else {
		local startyr = 2014
		local endyr = `startyr'
	}
}
else {
	local startyr = 1990
	local endyr = 2020
	local savefile = 1
}
if missing("`savetemp'") {
	local savetemp = 0
}

* Check if programs created by ipeds_cip_merge are available:
capture confirm file "./`temppath'/"
if _rc {
	shell mkdir "./`temppath'"
	do "`codepath'/ipeds_cip_merge.do"
}

* initialize dataset
clear all
tempfile master_data
save `master_data', emptyok

forvalues yr = `startyr'/`endyr' {

	di "********"
	di "* `yr' *"
	di "********"

	* for cip codes
	if `yr' < 1990 {
	local startyr = 1985
	local endyr = 1990		
	}
	else if `yr' >= 1990 & `yr' < 2000 {
	local startyr = 1990
	local endyr = 2000		
	}
	else if `yr' >= 2000 & `yr' < 2010 {
	local startyr = 2000
	local endyr = 2010	
	}

	* Adjust for file names
	if (`yr' <= 1994 & `yr' != 1990) {
		*local fyr = "c`yr'_cip_data_stata"
		local fyr = "c`yr'_cip"
	}
	else if `yr' == 1990 {
		local fyr = "c8990cip"
	}
	else if (`yr' >= 1995 & `yr' <=1999) {
		local fn = (`yr'-1900-1)*100 + (`yr'-1900)
		*local fyr = "c`fn'_a_data_stata"
		local fyr = "c`fn'_a"
	}
	else if (`yr' >= 2000 & `yr' <= 2005) {
		local fyr = "c`yr'_a"
	}
	else if (`yr' >= 2006 & `yr' <= 2011) {
		local fyr = "c`yr'_a_data_stata"
	}
	else if (`yr' != 2016 & (`yr' >= 2012 & `yr' <= 2017)) {
		local fyr = "c`yr'_a_rv_data_stata"
	}
	else if `yr' == 2016 {
		local fyr = "c`yr'_a_rv"
	}
	else if `yr' >= 2018 {
		local fyr = "c`yr'_a_data_stata"
	}

	* keep extra variables in years after 2007
	if `yr' < 2001 {
		local keepvars ctotalm ctotalw
	}
	else {
		local keepvars majornum ctotalm ctotalw
	}

	di "reading `fyr'..." 
	qui import delimited using "`rawpath'/`yr'/`fyr'.csv", clear varnames(nonames)

		* this is a work around to keep leading zeros
		qui ds *
		foreach var of varlist `r(varlist)' {
			local varname : di `var'
			rename `var' `varname'
		}
		qui drop in 1
		qui rename *, lower

		* rename variables so they are consistent
		if `yr' <= 2007 {
			rename crace15 ctotalm
		 	rename crace16 ctotalw
		}

		* if there's no dot in the cip code, create a dot. also trim values
		qui replace cipcode = strtrim(cipcode)
		gen ciplen = strlen(cipcode)
		qui summ ciplen
		if `r(max)' == 6 {
			qui replace cipcode = substr(cipcode,1,2) + "." + substr(cipcode,3,.)
		}
		drop ciplen
	

	keep unitid cipcode awlevel `keepvars'
	gen year = `yr'
	qui destring awlevel, replace
	capture destring majornum, replace

	

	* locals to flag all aggregate cips 
	local agg_cips (cipcode == "99.0000" | cipcode == "95.0000" | cipcode == "95.9500" | cipcode == "99." | cipcode == "99")
	local not_agg_cips (cipcode != "99.0000" & cipcode != "95.0000" & cipcode != "95.9500" & cipcode != "99." & cipcode != "99")

	* useful variables for checking how much data are lost
	qui destring ctotal*, replace
	egen ctot = rowtotal(ctotalm ctotalw)
	qui egen tot = total(ctot) if `not_agg_cips'


	* merge in the updated cipcode for years before 2010 (will need to repeat this)
	* start here!
	if `yr' < 2010 {
		* merge in appropriate `yr' cipcodes
		gen cipcode`startyr'_d`yr' = cipcode
		qui merge m:1 cipcode`startyr'_d`yr' using "`temppath'/cip`yr'"
		qui drop if _merge == 2
		qui count if _merge == 1 & `not_agg_cips' 
		if `r(N)' != 0 {
			di "Missing " `r(N)' " observations from dictionary."
			qui levelsof cipcode if _merge == 1 & `not_agg_cips', clean local(miss_cip)
			di "Missing CIP codes: " "`miss_cip'"
		}
		else {
			assert `agg_cips' if _merge == 1 
		}
		drop _merge cipcode`startyr'_d`yr' ciptitle`startyr' ciptitle`startyr'_d update_flag
	}
	* merge in the 2000 cipcodes for 1990 data
	if `yr' < 2000 {
		* merge in 2000 cipcodes
		qui merge m:1 cipcode1990 using "`temppath'/crosswalk1990to2000"
		qui drop if _merge == 2
		* note that you might have cipcodes that are missing here; these are the ones 
		* I check for at the end of the merge file
		* Find number and percent of missing observations
		qui count if cipcode2000=="" & cipdelete != 1 & `not_agg_cips'
		local miss_cip = `r(N)'
		* percent of data
		qui count if cipdelete != 1 & `not_agg_cips'
		local perc = (`miss_cip'/`r(N)')*100
		* percent of students
		qui egen tot_miss = total(ctot) if cipcode2000 == "" & cipdelete != 1 & `not_agg_cips'
		qui summ tot_miss
		local miss_student = `r(mean)'
		qui summ tot
		local student = `r(mean)'
		local perc_student = (`miss_student'/`student')*100
		di %7.0fc `miss_cip' " observations missing 2000 CIP codes (" %4.2fc `perc' "% of data; " %4.2fc `perc_student' "% of students)"  
		* drop variables
		drop _merge ciptitle1990_cw ciptitle2000_cw cipdelete tot_miss
	}

	if `yr' < 2010 {
		qui merge m:1 cipcode2000 using "`temppath'/crosswalk2000to2010"
		qui drop if _merge == 2
		* Find number and percent of missing observations
		qui count if cipcode2010=="" & `not_agg_cips'
		local miss_cip = `r(N)'
		qui count if `not_agg_cips'
		local perc = (`miss_cip'/`r(N)')*100
		* percent of students missing
		qui egen tot_miss = total(ctot) if cipcode2010 == "" & cipdelete != 1 & `not_agg_cips'
		qui summ tot_miss
		if `r(N)' != 0 {
			local miss_student = `r(mean)'
			qui summ tot
			local student = `r(mean)'
			local perc_student = (`miss_student'/`student')*100
		}
		else {
			local perc_student = 0
		}

		di %7.0fc `miss_cip' " observations missing 2010 CIP codes (" %4.2fc `perc' "% of data; " %4.3fc `perc_student' "% of students)"  
		* drop unnecessary variables
		drop _merge ciptitle2000_cw ciptitle2010_cw cipdelete Action Textchang tot_miss
	}
	if `yr' >= 2010 {
		gen cipcode2010 = cipcode
	}

	keep year unitid cipcode awlevel `keepvars' cipcode2010

	qui append using `master_data'
	qui save `"`master_data'"', replace
}

order year unitid cipcode cipcode2010 awlevel majornum
sort unitid cipcode awlevel year majornum

* save main version of file
if `savefile' == 1 {
	qui save "`savepath'/ipeds_c_all.dta", replace
}

* if desired, save a temporary version of data for cross section
if `savetemp' == 1 {
	qui export delimited "`temppath'/ipeds_c_temp.csv", replace
}

* remove temporary folders, unless otherwise specfied
if $rm_temp_dir {
	shell rm -rf "./`temppath'/"
}

