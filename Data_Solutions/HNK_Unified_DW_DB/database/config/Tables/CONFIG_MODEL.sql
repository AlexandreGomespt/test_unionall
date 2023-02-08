CREATE TABLE [config].[CONFIG_MODEL] (
    [PK_CONFIG_MODEL]           INT            NOT NULL,
    [MODEL_NAME]                NVARCHAR (255) NOT NULL,
    [PERIODICITY]               NVARCHAR (255) NULL,
    [DT_LAST_SUCCESS_EXECUTION] DATETIME       NULL,
    [DT_NEXT_EXECUTION]         DATETIME       NULL,
    [FLG_IS_ACTIVE]             BIT            NOT NULL,
    [DT_CREATED]                DATETIME       DEFAULT (getdate()) NOT NULL,
    [CREATED_BY]                NVARCHAR (255) DEFAULT ((1)) NOT NULL,
    [DT_MODIFIED]               DATETIME       DEFAULT (getdate()) NOT NULL,
    [MODIFIED_BY]               NVARCHAR (255) DEFAULT ((1)) NOT NULL,
    PRIMARY KEY CLUSTERED ([PK_CONFIG_MODEL] ASC)
);

