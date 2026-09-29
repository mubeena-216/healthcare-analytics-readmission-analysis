
------------Healthcare Analytics & Readmission Analysis------------
----                 SQL Analysis - SQLite       ----
    
--            Total Encounters

select count(*) as total_encounters
from healthcare_data_cleaned;

--          Total Unique Patients

SELECT count(distinct patient_nbr) as total_patients
from healthcare_data_cleaned;

--         Repeated Patients

select count(*) as total_repeat_patients
from (select patient_nbr
      from healthcare_data_cleaned
	  group by patient_nbr
	  having count(*) > 1);
	  
--        Repeat Patients Rate

select count(*) as total_patients,
sum(encounter_count > 1) as  repeat_patients,
round(
      (sum(encounter_count > 1) * 1.0 / count(*)) * 100,2) as repeat_patient_rate
FROM(
     select patient_nbr,count(*) as encounter_count
	 from healthcare_data_cleaned
	 group by patient_nbr
	 );

--            Average length of stay

SELECT round(avg(time_in_hospital),2) as avg_length_of_stay
from healthcare_data_cleaned;

--            Average medications

SELECT round(avg(num_medications),2) as average_medications
from healthcare_data_cleaned;

-- top 10 patients have highest hospital utilization

SELECT patient_nbr, 
       sum(total_prior_visits) as total_utilization
FROM healthcare_data_cleaned
group by patient_nbr
order by total_utilization desc
limit 10;

--    How does readmission vary by diagnosis grp  (how many pts fall into readmission category)

select diagnosis_category,
      readmitted,
	  count(*) total_encounters
from healthcare_data_cleaned
group by diagnosis_category,readmitted
order by diagnosis_category,
      readmitted desc;
	  
-- WHICH DIAGNOSIS GRPS HAVE HIGHEST READMISSION RATE  (30 day readmitted encounter/ total encounter in that diagnosis )

select diagnosis_category,
       readmit_30,
	   count(*) as total_encounters,
	   sum(readmit_30) as readmitted_30,
	   round(
	   (sum (readmit_30)* 1.0 / count(*) ) *100 , 2 
	   ) as readmission_rate
from healthcare_data_cleaned
group by diagnosis_category
order by readmission_rate desc;

--   FOR EACH PATIENT WHAT WAS THEIR PREVIOUS encounter( inside lag encounterid as it want to knw encounter
SELECT patient_nbr,
      encounter_id,
      lag(encounter_id) over(
	            partition by patient_nbr
				order by encounter_id
				) as  previous_encounter
				
from healthcare_data_cleaned;

-- RANK PATIENTS BY HOSPITAL UTILIZATION

with patient_utilization as (select patient_nbr,
       sum(total_prior_visits) as total_utilization
from healthcare_data_cleaned
group by patient_nbr
order by total_utilization desc )

SELECT *,
      dense_rank() over(
	                 order by total_utilization desc
					 ) as utilization_rank
from patient_utilization;

-- FIND SECOND HIGHEST UTILIZATION PATIENT

with patient_utilization as (
   SELECT patient_nbr,
          sum(total_prior_visits) as total_utilization
   from healthcare_data_cleaned
   group by patient_nbr
    ) ,
   
   ranked_patients as (
   select *,
          dense_rank() over(
		            order by total_utilization desc) as utilization_rank
   from patient_utilization
   )
   SELECT *
   from ranked_patients
   where utilization_rank = 2;
   
---  WHICH DIAGNOSIS GRPS HAVE 30 DAY READMISSION RATE ABOVE OVERALL HOSPITAL RATE
-----        30 day readmission/ total encounters *100

with overall_rate as (
    SELECT sum(readmit_30) as total_readmissions,
	       count(*) as total_encounters,
		   round(
		   ( sum(readmit_30) *1.0 /  count(*)  ) *100 ,2		   
		   ) as overall_rate
	from healthcare_data_cleaned) ,
	
	readmission_rate as (
	select diagnosis_category,
	       round(
		   ( sum(readmit_30) *1.0 /  count(*)  ) *100 ,2		   
		   ) readmission_rate
	from healthcare_data_cleaned
	group by diagnosis_category
	)
select r.diagnosis_category,
        r.readmission_rate,
		o.overall_rate
		
from  overall_rate as o
cross join readmission_rate as r
where r.readmission_rate > o.overall_rate
order by r.readmission_rate desc;

---- AVG LOS BY DIAGNOSIS AND READMISSION

select diagnosis_category,
       readmitted,
	   round(Avg(time_in_hospital), 2) as avg_length_of_stay
from healthcare_data_cleaned
group by diagnosis_category,readmitted
order by avg_length_of_stay desc;

--- ENCOUNTERS(ptZ) MEDICATION CHANGED RELATE TO 30 DAY READMISSION

select medication_changed,
       count(*) as total_encounters,
	   sum(readmit_30) as readmitted_30,
	   round(
	   (sum(readmit_30) *1.0 / count(*)) *100 ,2   
	   ) as readmission_rate
from healthcare_data_cleaned
group by medication_changed;












   
