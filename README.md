```sh
uv init
uv venv --python 3.9
source .venv/bin/activate
# uv add fastapi uvicorn pydantic-settings requests sqlmodel python-jose
uv pip install -r pyproject.toml
python run.py 8200
# pm2 start run.py --name ig_backend --interpreter .venv/bin/python3 -- 8200 -i 1
pm2 start ecosystem.config.js
# pm2 logs ig_backend
# pm2 restart ig_backend
```

```
https://www.instagram.com/oauth/authorize?enable_fb_login=0&force_authentication=1&client_id=560330529919299&redirect_uri=https://xkaxserbfdmtajhq.tunnel-pt.elice.io/&response_type=code&scope=instagram_business_basic%2Cinstagram_business_manage_messages%2Cinstagram_business_manage_comments%2Cinstagram_business_content_publish
```