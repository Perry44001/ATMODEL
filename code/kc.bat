set "BASE_DIR=E:/ATCHATGROOP/ATMODEL/code/"
set "CONDA_ENV=FtAcstMd"
set "PYTHON_SCRIPT=xunfeiMd.py"
SET "BASE_PATH=E:/ATCHATGROOP/ATMODEL/data/"
SET "OUT_PATH=E:/ATCHATGROOP/ATMODEL/kcdata/"

cd /d "%BASE_DIR%"

@REM call conda info --envs | findstr /C:"%CONDA_ENV%" > nul
@REM if errorlevel 1 (
@REM     echo env no activated, starting...
@REM     conda activate %CONDA_ENV%
@REM ) else (
@REM     echo env already activated.
@REM )

for %%p in (
    "xxu.json"
    "20211207-20220617.json"
    "20220617-20240103.json"
    "20240103-20240705.json"
) do (
    echo %%p
    set "FULLIN_PATH=%BASE_PATH%%%p"
    echo Full input path: %FULLIN_PATH%
    set "FULLOUT_PATH=%OUT_PATH%kc%%p"
    echo Full output path: %FULLOUT_PATH%
    python %PYTHON_SCRIPT% -i %FULLIN_PATH% -o %FULLOUT_PATH%  
)

conda deactivate

echo done.
pause