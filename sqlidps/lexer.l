
%{
#include "./wrapper.h"  
%}

%option noyywrap
%option caseless


DIGIT           [0-9]
LETTER          [a-zA-Z]
ID              {LETTER}([a-zA-Z0-9$_])*
STRING_SINGLE   \'([^\\\']|(\\.))*\'
STRING_DOUBLE   \"([^\\\"]|(\\.))*\'
BACKTICK        \`([^\\\`]|(\\.))*\`
WHITESPACE      [ \t\r\n]+
COMMENT         (\/\*([^*]|\*+[^*/])*\*+\/)|(--[^\n]*)|(#.*)
KEYWORDS        (ALTER|AND|AS|AUTO_INCREMENT|BEGIN|BREAK|BY|CASE|CHECK|CHECKPOINT|COMMENT|COMMIT|CREATE|CURSOR|DATABASE|DBCC|DEFAULT|DELETE|DENY|DISTINCT|DROP|ELSE|END|ENGINE|EXISTS|EXEC|EXECUTE|FROM|FULL|FUNCTION|GO|GRANT|GROUP|HAVING|IF|IN|INDEX|INNER|INSERT|JOIN|KEY|LEFT|LIKE|LIMIT|NOT|NULL|ON|OPENQUERY|OPENROWSET|OPENDATASOURCE|OR|ORDER|OUTER|PRIMARY|PROCEDURE|REFERENCES|RIGHT|SELECT|SET|SHUTDOWN|SP_|TABLE|THEN|TRAN|TRANSACTION|TRIGGER|UNION|UPDATE|USE|VALUES|VIEW|WHEN|WHERE|WHILE|OFFSET|ALL|ANY)
FUNCTIONS       (ASCII\(.*\)|BENCHMARK\(.*\)|BULK[[:space:]]+INSERT|CHAR\(.*\)|CHR\(.*\)|CONCAT\(.*\)|dbms_pipe\.receive_message\(.*\)|INTO[[:space:]]+DUMPFILE|LOAD[[:space:]]+DATA[[:space:]]+INFILE|LOAD_FILE\(.*\)|OPENROWSET|pg_sleep\(.*\)|SLEEP\(.*\)|sp_password|SYS\.DBMS_LDAP\.INIT|UTL_HTTP\.REQUEST|UTL_INADDR\.get_host_addr|version\(.*\)|database\(.*\)|substring\(.*\)|WAITFOR[[:space:]]+DELAY)
DATA_EXFIL      (@@version|version\(.*\)|sqlite_version\(.*\)|product_component_version|information_schema\.tables|information_schema\.columns|sys\.objects|sys\.columns|sysobjects|syscolumns|all_tables|all_col_comments|ascii\(.*\)|char\(.*\)|chr\(.*\)|concat\(.*\)|concat_ws\(.*\)|group_concat\(.*\)|mid\(.*\)|substring\(.*\)|left\(.*\)|right\(.*\)|hex\(.*\)|unhex\(.*\)|cast\(.*\)|convert\(.*\))
BLINDSQLI       (if\(.*\)|case[[:space:]]+when[[:space:]]+then[[:space:]]+else[[:space:]]+end|iif\(.*\)|sleep\(.*\)|pg_sleep\(.*\)|waitfor[[:space:]]+delay|benchmark\(.*\)|dbms_pipe\.receive_message\(.*\)|get_lock\(.*\)|rlike|regexp)
ERRORBASED      (EXTRACTVALUE\(.*\)|UPDATEXML\(.*\)|exp\(.*\)|FLOOR\(.*\)|count\(.*\)|rand\(.*\))
FILEBASED       (LOAD_FILE\(.*\)|INTO[[:space:]]+OUTFILE|INTO[[:space:]]+DUMPFILE|LOAD[[:space:]]+DATA[[:space:]]+INFILE|xp_cmdshell|xp_dirtree|xp_fileexist|xp_regread|xp_regwrite|xp_servicecontrol|sp_oacreate|sp_oamethod|sp_makewebtask|sp_addextendedproc|COPY[[:space:]]+\.\.\.[[:space:]]+FROM[[:space:]]+PROGRAM|lo_import\(.*\)|lo_export\(.*\)|dblink_connect\(.*\)|dblink_exec\(.*\)|UTL_FILE|DBMS_JAVA\.runjava\(.*\)|DBMS_LOB\.LOADFROMFILE\(.*\)|BACKUP[[:space:]]+DATABASE[[:space:]]+TO[[:space:]]+DISK)
DBMS_ID_KEYS    (@@CONNECTIONS|@@CPU_BUSY|USER_ID\(.*\)|ROWNUM|RAWTOHEX\(.*\)|LNNVL\(.*\)|pg_client_encoding\(.*\)|current_database\(.*\)|sqlite_version\(.*\)|connection_id\(.*\)|crc32\(.*\))
ADV_NET_FUNCS   (UTL_HTTP\.REQUEST\(.*\)|UTL_INADDR\.GET_HOST_ADDRESS\(.*\)|UTL_TCP\.AVAILABLE\(.*\))
OPERATORS       (<>|<=|>=|!=|=|<|>|!|\*|\/|\+|\-)
PUNCTUATION     (\(|\)|,|\.)

%%
{WHITESPACE}              ;  
{COMMENT}                 { append_token("COMMENT"); }
{KEYWORDS}                { append_token("KEYWORD"); }
{FUNCTIONS}               { append_token("FUNCTIONS"); }
{DATA_EXFIL}              { append_token("DATA_EXFIL"); }
{BLINDSQLI}               { append_token("BLINDSQLI"); }
{ERRORBASED}              { append_token("ERRORBASED"); }
{FILEBASED}               { append_token("FILEBASED"); }
{DBMS_ID_KEYS}            { append_token("DBMS_ID_KEYS"); }
{ADV_NET_FUNCS}           { append_token("ADV_NET_FUNCS"); }
"@@"{LETTER}({LETTER}|{DIGIT}|\$|_)*   { append_token("SYSTEM_VARIABLE"); }
"@"{LETTER}({LETTER}|{DIGIT}|\$|_)*    { append_token("VARIABLE"); }
{DIGIT}+(\.{DIGIT}+)?     { append_token("NUMBER"); }
{STRING_SINGLE}           { append_token("STRING"); }
{STRING_DOUBLE}           { append_token("STRING"); }
{BACKTICK}                { append_token("IDENTIFIER"); }
{ID}                      { append_token("IDENTIFIER"); }
{OPERATORS}               { append_token("OPERATOR"); }
";"                       { append_token("EOS"); }
{PUNCTUATION}             { append_token("PUNCTUATION"); }
.                         { append_token("UNKNOWN"); }
%%

