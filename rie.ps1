$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$ScriptDir\rie.py" @args
