-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/dFEb8N
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.
DROP TABLE "df_PGE";
DROP TABLE "df_SCE";
DROP TABLE "df_SDGE";

CREATE TABLE "df_PGE" (
    "Utility" varchar(5)   NOT NULL,
    "Service_City" varchar(25)   NOT NULL,
    "Service_Zip" float   NOT NULL,
    "Service_County" varchar(25)   NOT NULL,
    "Technology_Type" varchar(25)   NOT NULL,
    "System_Size_AC" float,
    "Storage_Size_kW_AC" float,
    "Inverter_size_kW_AC" float,
    "Mounting_Method" varchar(10)   NOT NULL,
    "App_Received_Date" date   NOT NULL,
    "Installer_Name" varchar(25)   NOT NULL,
    "Third_Party_Owned" varchar(3),
    "Electric_Vehicle" varchar(3)   NOT NULL,
    "Total_System_Cost" float   NOT NULL,
    "Generator_Manufacturer" varchar(25)   NOT NULL,
    "Inverter_Manufacturer" varchar(25)   NOT NULL,
    "Generator_Quantity" float   NOT NULL,
    "Inverter_Quantity" float   NOT NULL
);

CREATE TABLE "df_SCE" (
    "Utility" varchar(5)   NOT NULL,
    "Service_City" varchar(25)   NOT NULL,
    "Service_Zip" float   NOT NULL,
    "Service_County" varchar(25)   NOT NULL,
    "Technology_Type" varchar(25)   NOT NULL,
    "System_Size_AC" float,
    "Storage_Size_kW_AC" float,
    "Inverter_size_kW_AC" float,
    "Mounting_Method" varchar(10)   NOT NULL,
    "App_Received_Date" date   NOT NULL,
    "Installer_Name" varchar(25)   NOT NULL,
    "Third_Party_Owned" varchar(3),
    "Electric_Vehicle" varchar(3)   NOT NULL,
    "Total_System_Cost" float   NOT NULL,
    "Generator_Manufacturer" varchar(25)   NOT NULL,
    "Inverter_Manufacturer" varchar(25)   NOT NULL,
    "Generator_Quantity" float   NOT NULL,
    "Inverter_Quantity" float   NOT NULL
);

CREATE TABLE "df_SDGE" (
    "Utility" varchar(5)   NOT NULL,
    "Service_City" varchar(25)   NOT NULL,
    "Service_Zip" float   NOT NULL,
    "Service_County" varchar(25)   NOT NULL,
    "Technology_Type" varchar(25)   NOT NULL,
    "System_Size_AC" float,
    "Storage_Size_kW_AC" float,
    "Inverter_size_kW_AC" float,
    "Mounting_Method" varchar(10)   NOT NULL,
    "App_Received_Date" date   NOT NULL,
    "Installer_Name" varchar(25)   NOT NULL,
    "Third_Party_Owned" varchar(3),
    "Electric_Vehicle" varchar(3)   NOT NULL,
    "Total_System_Cost" float   NOT NULL,
    "Generator_Manufacturer" varchar(25)   NOT NULL,
    "Inverter_Manufacturer" varchar(25)   NOT NULL,
    "Generator_Quantity" float   NOT NULL,
    "Inverter_Quantity" float   NOT NULL
);

