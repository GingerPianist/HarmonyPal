## Jak uruchomić sam harmonizator na przykładzie
1. Należy pobrać repozytorium z GH: https://github.com/GingerPianist/HarmonyPal
2. Pobrać i rozpakować model: https://drive.google.com/file/d/1v5iaw_sf0HgEaeOntVIIerykm5BGGf8y/view
3. Zainstalować wymagania z pliku requirements.txt (python 3.8)
3. Odpalić komendę:
	`python3 inference.py \
        --configuration=config/emopia_finetune.yaml \
        --representation=functional \
        --key_determine=rule \
        --inference_params=emo_harmonizer_ckpt_functional/best_params.pt \
        --output_dir=generation/emopia_functional_rule`

## Jak uruchomić pipeline harmonizujący (prawie działa, jest jakiś problem z importami)
1. Należy pobrać repozytorium z GH: https://github.com/GingerPianist/HarmonyPal
2. Pobrać i rozpakować model: https://drive.google.com/file/d/1v5iaw_sf0HgEaeOntVIIerykm5BGGf8y/view
3. Zainstalować wymagania z pliku requirements.txt (python 3.8)
4. Wywołać harmonyPal.py: `python3 harmonyPal.py --audio_file <ścieżka do pliku>`
