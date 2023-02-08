﻿CREATE TABLE [config].[CONFIG_FILE] (
    [PK_CONFIG_FILE]          INT            IDENTITY (1, 1) NOT NULL,
    [INPUT_FILENAME]          NVARCHAR (255) NOT NULL,
    [INPUT_FILE_PATH]         NVARCHAR (255) NOT NULL,
    [NUMBER_OF_COLUMNS]       INT            NOT NULL,
    [DELIMITER]               NVARCHAR (255) NULL,
    [DESTIONATION_TABLE_NAME] NVARCHAR (255) NULL,
    [DT_CREATED]              DATETIME       DEFAULT (getdate()) NOT NULL,
    [CREATED_BY]              NVARCHAR (255) DEFAULT ((1)) NOT NULL,
    [DT_MODIFIED]             DATETIME       DEFAULT (getdate()) NOT NULL,
    [MODIFIED_BY]             NVARCHAR (255) DEFAULT ((1)) NOT NULL,
    PRIMARY KEY CLUSTERED ([PK_CONFIG_FILE] ASC)
);
