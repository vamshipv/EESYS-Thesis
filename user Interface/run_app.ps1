# Start the explorer app with the thesis env (not the global Python).
# Usage from anywhere:  & "<path>\master code\user Interface\run_app.ps1"
$streamlit = Join-Path $HOME ".venvs\eesys-thesis\Scripts\streamlit.exe"
if (-not (Test-Path $streamlit)) { throw "Thesis env not found: $streamlit" }
& $streamlit run (Join-Path $PSScriptRoot "explore_app.py")
