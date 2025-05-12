NUMERO_INVALIDO = "Numero de tweet invalido."
SELECCION = "Seleccione una opcion:"
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS_MENSAJE = "Tweets eliminados:"
ATRAS = "**"
MENU = """Seleccione una opcion:

1. Crear Tweet
2. Buscar Tweet
3. Eliminar Tweet
4. Salir
"""


# -----------------------------------------------------------------------------


def main():
    id = 0
    tweets = {}
    tokens_ids = {}
    while True:
        opcion = input(MENU)
        if opcion == "1":
            nuevo_tweet = crear_tweet(id, tweets, tokens_ids)
            if nuevo_tweet:
                id += 1
            continue
        if opcion == "2":
            buscar_tweet(tweets, tokens_ids, "buscar")
            continue
        if opcion == "3":
            eliminar_tweet(tweets, tokens_ids)
            continue
        if opcion == "4":
            print(FIN)
            break
        print(INPUT_INVALIDO)


# -----------------------------------------------------------------------------


def verificar_ir_atras(opcion_input):
    return opcion_input == ATRAS


# -----------------------------------------------------------------------------


def crear_tweet(id, tweets, tokens_ids):
    tweet_normalizado = pedir_y_agregar_tweet(id, tweets)
    if not tweet_normalizado:
        return False
    agregar_tokens_indexados(id, tokens_ids, tweet_normalizado)
    print(f"OK {id}")
    return True


# -----------------------------------------------------------------------------


def pedir_y_agregar_tweet(id, tweets):
    while True:
        tweet = input("Ingrese el tweet a almacenar:\n")
        if verificar_ir_atras(tweet):
            return False
        tweet_normalizado = normalizar_texto(tweet)
        if tweet_normalizado.strip() == "":
            print(INPUT_INVALIDO)
            continue
        tweets[id] = tweet
        return tweet_normalizado


# -----------------------------------------------------------------------------


def normalizar_texto(texto):
    texto = texto.lower()
    tweet_normalizado = ""

    letras_con_tilde = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ä": "a",
        "ë": "e",
        "ï": "i",
        "ö": "o",
        "ü": "u",
    }

    for letra in texto:
        if not (letra.isalnum() or letra == " "):
            continue
        elif letra in letras_con_tilde:
            tweet_normalizado += letras_con_tilde[letra]
            continue
        tweet_normalizado += letra

    return tweet_normalizado


# -----------------------------------------------------------------------------


def tokenizar_por_segmentos(palabras):
    segmentos = []

    for palabra in palabras:
        if len(palabra) >= 3:
            for i in range(len(palabra)):
                longitud = i + 3
                while longitud <= len(palabra):
                    if palabra[i:longitud] not in segmentos:
                        segmentos.append(palabra[i:longitud])
                    longitud += 1
        else:
            segmentos.append(palabra)

    return segmentos


# -----------------------------------------------------------------------------


def agregar_tokens_indexados(id_tweet, tokens_ids, tweet_normalizado):
    palabras = tweet_normalizado.split()
    tokens = tokenizar_por_segmentos(palabras)

    for token in tokens:
        if token not in tokens_ids:
            tokens_ids[token] = [id_tweet]
        elif id_tweet not in tokens_ids[token]:
            tokens_ids[token].append(id_tweet)


# ---------------------------------------------------------------------------


def buscar_tweet(tweets, tokens_ids, accion):
    while True:
        if accion == "buscar":
            palabras = input("Ingrese la/s palabra/s clave a buscar:\n")
        else:
            palabras = input("Ingrese el tweet a eliminar:\n")

        if verificar_ir_atras(palabras):
            return False

        palabras_normalizadas = normalizar_texto(palabras).strip()

        if palabras_normalizadas == "":
            print(INPUT_INVALIDO)
            continue

        palabras_normalizadas = palabras_normalizadas.split()

        ids_resultantes = encontrar_y_mostrar_tweets(
            palabras_normalizadas, tokens_ids, tweets
        )

        if not ids_resultantes:
            print(NO_ENCONTRADOS)
            return False

        return ids_resultantes


# ---------------------------------------------------------------------------


def encontrar_y_mostrar_tweets(palabras, tokens_ids, tweets):
    ids_palabras = []
    for palabra in palabras:
        if palabra not in tokens_ids:
            return False
        if tokens_ids[palabra] not in ids_palabras:
            ids_palabras.append(tokens_ids[palabra])

    ids_resultantes = []
    if len(ids_palabras) == 1:
        mostrar_tweets(ids_palabras[0], tweets)
        return ids_palabras[0]
    for id in ids_palabras[0]:
        agregar = True
        for sub_id in ids_palabras[1:]:
            if id not in sub_id:
                agregar = False
                break
        if agregar:
            ids_resultantes.append(id)

    if ids_resultantes == []:
        return False

    ids_resultantes = set(ids_resultantes)

    mostrar_tweets(ids_resultantes, tweets)
    return ids_resultantes


# ---------------------------------------------------------------------------


def mostrar_tweets(ids, tweets):
    print(RESULTADOS_BUSQUEDA)
    for id in ids:
        print(f"{id}. {tweets[id]}")


# ---------------------------------------------------------------------------


def eliminar_tweet(tweets, tokens_ids):
    while True:
        tweets_encontrados = buscar_tweet(tweets, tokens_ids, "eliminar")
        if not tweets_encontrados:
            break
        while True:
            ids = input("Ingrese los numeros de tweets a eliminar:\n")
            if verificar_ir_atras(ids):
                break
            ids = ids.split(",")
            ids_normalizadas = normalizar_ids(ids)
            if not ids_normalizadas:
                print(INPUT_INVALIDO)
                continue
            ids_normalizadas = set(ids_normalizadas)
            tweets_eliminados = eliminar_tweet_e_ids_de_tokens(
                ids_normalizadas, tweets, tokens_ids
            )
            if not tweets_eliminados:
                print(NUMERO_INVALIDO)
                continue
            mostrar_tweets_eliminados(tweets_eliminados)
            break
        break


# ---------------------------------------------------------------------------


def normalizar_ids(ids):
    ids_normalizadas = []

    for i in range(len(ids)):
        if "-" in ids[i] and ids[i].count("-") == 1:
            rango = ids[i].split("-")
            num1 = rango[0].strip()
            num2 = rango[1].strip()
            if num1 <= num2 and num1.isnumeric() and num2.isnumeric():
                for sub_i in range(int(num1), int(num2) + 1):
                    ids_normalizadas.append(sub_i)
            else:
                return False
        elif not ids[i].strip().isnumeric():
            return False
        else:
            ids_normalizadas.append(int(ids[i]))

    return ids_normalizadas


# ---------------------------------------------------------------------------


def eliminar_tweet_e_ids_de_tokens(ids, tweets, tokens_ids):
    for id in ids:
        if id not in tweets:
            return False

    tweets_eliminados = {}

    for id in ids:
        tweet_normalizado = normalizar_texto(tweets[id])
        palabras = tweet_normalizado.split(" ")
        tokens = tokenizar_por_segmentos(palabras)
        tweets_eliminados[id] = tweets[id]

        for token in tokens:
            if len(tokens_ids[token]) > 1:
                tokens_ids[token].remove(id)
            else:
                tokens_ids.pop(token)

        tweets.pop(id)
    return tweets_eliminados


# ---------------------------------------------------------------------------


def mostrar_tweets_eliminados(tweets):
    print(TWEETS_ELIMINADOS_MENSAJE)
    for tweet in tweets:
        print(f"{tweet}. {tweets[tweet]}")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
