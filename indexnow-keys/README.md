# IndexNow keys

Each `<site>.txt` must be uploaded to that site's web root so it is reachable at:

```
https://<site>/<key>.txt        (file content = the key itself)
```

IndexNow verifies this file before accepting submissions. Until a file is
hosted, that site is simply skipped (the push step is `continue-on-error`).

## Keys generated

- **algeriacertify.com** → `https://algeriacertify.com/c4e42e19587bf3bbef23c3a8ac0f6bae.txt`
- **tkawen.com** → `https://tkawen.com/ceb683a9c7e71b2d7ff52c4728451aa3.txt`
- **liqaa.io** → `https://liqaa.io/0de4f1a2aa4c66011b516be1ca239406.txt`
- **pharmapro.tkawen.com** → `https://pharmapro.tkawen.com/d809735a48e352844e028fb3478155f3.txt`
- **catalogue.tkawen.com** → `https://catalogue.tkawen.com/c853d03cd303883092cbb16608a90a63.txt`

## Upload (Laravel sites on the VPS)

Drop each file into the app's `public/` dir, e.g.:

```bash
echo "c4e42e19587bf3bbef23c3a8ac0f6bae" > /var/www/<app>/public/c4e42e19587bf3bbef23c3a8ac0f6bae.txt   # algeriacertify.com
echo "ceb683a9c7e71b2d7ff52c4728451aa3" > /var/www/<app>/public/ceb683a9c7e71b2d7ff52c4728451aa3.txt   # tkawen.com
echo "0de4f1a2aa4c66011b516be1ca239406" > /var/www/<app>/public/0de4f1a2aa4c66011b516be1ca239406.txt   # liqaa.io
echo "d809735a48e352844e028fb3478155f3" > /var/www/<app>/public/d809735a48e352844e028fb3478155f3.txt   # pharmapro.tkawen.com
echo "c853d03cd303883092cbb16608a90a63" > /var/www/<app>/public/c853d03cd303883092cbb16608a90a63.txt   # catalogue.tkawen.com
```
