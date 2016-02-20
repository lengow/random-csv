# random-csv

Generate a random CSV file with a schema.

## Features

* Provide a schema with `int`, `float` or `str`
* Can supply filemask to name file (extension is always txt for now)
* Can add datetime stamp to filename (useful for many files)
* Can supply seed for repeated result

## Usage

Get help with `-h`

Example usage:

```python
python generate_csv.py 11 --filemask=test --addtimestamp --delimiter=, --how-many=1 --seed=42 int int float str
```

generates (just 1 file)

```csv
686579303,119540831,0.025010755222666936,JFCrnl2edlBD
542621108,646412689,0.026535969683863625,z1C5Jau2RJtB
819795579,361415646,0.10221027651984871,WmTSHf6	pWkL
890566476,674996843,0.6185197523642461,UyifDLkDmWJ6
682560971,895619255,0.36483217897008424,VTAIjv	Fu7WI
993631208,687194506,0.6881619584333132,CPhDeOZIiBOB
703771909,536045484,0.39563190106066426,6sHrF	H2ZUCr
547099690,529908599,0.09090941217379389,gotu2iXW7 Gb
730448745,773869166,0.11455174298368664,	IRoL3u6aH#w
545119047,979926683,0.10641082279770497,"M#ztVu aP""co"
997612044,389747629,0.8787218778231842,"NEhEkk""i	qq8"

```
