-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/dFEb8N
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.
DROP TABLE IF EXISTS "CA";

CREATE TABLE "CA" (
    "Utility" varchar   NOT NULL,
    "Service_City" varchar   NOT NULL,
    "Service_Zip" varchar   NOT NULL,
    "Service_County" varchar   NOT NULL,
    "Technology_Type" varchar   NOT NULL,
    "System_Size_AC" float,
    "Storage_Size_kW_AC" float,
    "Inverter_size_kW_AC" float,
    "Mounting_Method" varchar   NOT NULL,
    "App_Received_Date" date   NOT NULL,
    "Installer_Name" varchar   NOT NULL,
    "Third_Party_Owned" varchar,
    "Electric_Vehicle" varchar   NOT NULL,
    "Total_System_Cost" float   NOT NULL,
    "Generator_Manufacturer" varchar   NOT NULL,
    "Inverter_Manufacturer" varchar   NOT NULL,
    "Generator_Quantity" float   NOT NULL,
    "Inverter_Quantity" float   NOT NULL,
	"Year" INT NOT NULL
);