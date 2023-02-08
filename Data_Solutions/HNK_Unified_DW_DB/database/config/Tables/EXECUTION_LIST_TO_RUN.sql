CREATE TABLE [config].[EXECUTION_LIST_TO_RUN] (
    [PK_EXECUTION_LIST_TO_RUN] INT            IDENTITY (1, 1) NOT NULL,
    [MODEL_NAME]               NVARCHAR (255) NULL,
    [GROUP_NAME]               NVARCHAR (255) NULL,
    [OBJECT_NAME]              NVARCHAR (255) NULL,
    [OBJECT_TYPE]              NVARCHAR (255) NOT NULL,
    [SOURCE_OBJECT_PATH]       NVARCHAR (255) NULL,
    [DESTINATION_OBJECT_PATH]  NVARCHAR (255) NULL,
    [PARAMETERS_LIST]          NVARCHAR (255) NULL,
    [MODEL_ORDER]              INT            NOT NULL,
    [GROUP_ORDER]              INT            NOT NULL,
    [OBJECT_ORDER]             INT            NOT NULL,
    [DT_CREATED]               DATETIME       DEFAULT (getdate()) NOT NULL,
    [CREATED_BY]               NVARCHAR (255) DEFAULT ((1)) NOT NULL,
    [DT_MODIFIED]              DATETIME       DEFAULT (getdate()) NOT NULL,
    [MODIFIED_BY]              NVARCHAR (255) DEFAULT ((1)) NOT NULL
);

