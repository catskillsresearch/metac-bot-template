How to run LLM server
=====================
1. Go to tensordock and spin up the instance
2. Login into the instance using the ssh command "ssh -p yyyyy -L 11434:localhost:11434 user@x.y.z.w".  Check on the tensordock server status plage for the exact IP address needed for the last part.
3. Run "docker start ollama"
4. Run "nvitop"
5. When done, run "sudo shutdown now"
