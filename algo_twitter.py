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
    if opcion_input == ATRAS:
        return True
    return False


# -----------------------------------------------------------------------------


def crear_tweet(id, tweets, tokens_ids):
    while True:
        tweet = input("Ingrese el tweet a almacenar:\n")
        if verificar_ir_atras(tweet):
            return False
        tweet_normalizado = normalizar_texto(tweet)
        if tweet_normalizado.strip() == "":
            print(INPUT_INVALIDO)
            continue
        tweets[id] = tweet
        agregar_tokens_indexados(id, tokens_ids, tweet_normalizado)
        print(f"OK {id}")
        return True


# -----------------------------------------------------------------------------


def normalizar_texto(texto):
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
    tweet_normalizado = texto.lower()
    for letra in tweet_normalizado:
        if not (letra.isalnum() or letra == " "):
            tweet_normalizado = tweet_normalizado.replace(letra, "")
        elif letra in letras_con_tilde:
            tweet_normalizado = tweet_normalizado.replace(
                letra, letras_con_tilde[letra]
            )

    return tweet_normalizado


# -----------------------------------------------------------------------------


def tokenizar_por_segmentos(tweet_tokenizado_por_palabras):
    tweet_tokenizado_por_segmentos = []
    for i in range(len(tweet_tokenizado_por_palabras)):
        if len(tweet_tokenizado_por_palabras[i]) >= 3:
            for sub_i in range(len(tweet_tokenizado_por_palabras[i])):
                longitud = sub_i + 3
                while longitud <= len(tweet_tokenizado_por_palabras[i]):
                    if (
                        tweet_tokenizado_por_palabras[i][sub_i:longitud]
                        not in tweet_tokenizado_por_segmentos
                    ):
                        tweet_tokenizado_por_segmentos.append(
                            tweet_tokenizado_por_palabras[i][sub_i:longitud]
                        )
                    longitud += 1
        else:
            tweet_tokenizado_por_segmentos.append(
                tweet_tokenizado_por_palabras[i]
            )

    for e in tweet_tokenizado_por_segmentos:
        if not e.isalnum():
            while e in tweet_tokenizado_por_segmentos:
                tweet_tokenizado_por_segmentos.remove(e)

    return tweet_tokenizado_por_segmentos


# -----------------------------------------------------------------------------


def agregar_tokens_indexados(id_tweet, tokens_ids, tweet_normalizado):
    tweet_tokenizado_por_palabras = tweet_normalizado.split(" ")
    lista_tokens = tokenizar_por_segmentos(tweet_tokenizado_por_palabras)

    for e in lista_tokens:
        if e not in tokens_ids:
            tokens_ids[e] = [id_tweet]
        elif id_tweet not in tokens_ids[e]:
            tokens_ids[e].append(id_tweet)


# ---------------------------------------------------------------------------


def buscar_tweet(tweets, tokens_ids, accion):
    while True:
        if accion == "buscar":
            palabras = input("Ingrese la/s palabra/s clave a buscar:\n")
        else:
            palabras = input("Ingrese el tweet a eliminar:\n")

        if verificar_ir_atras(palabras):
            return "atras"

        palabras_normalizadas = normalizar_texto(palabras).strip()
        lista_palabras = palabras_normalizadas.split(" ")
        while "" in lista_palabras:
            lista_palabras.remove("")

        if palabras_normalizadas == "":
            print(INPUT_INVALIDO)
            continue

        lista_ids_resultantes = encontrar_y_mostrar_tweets(
            lista_palabras, tokens_ids, tweets
        )

        if not lista_ids_resultantes:
            print(NO_ENCONTRADOS)
            return False

        return lista_ids_resultantes


# ---------------------------------------------------------------------------


def encontrar_y_mostrar_tweets(palabras, tokens_ids, tweets):
    lista_ids_palabras = []
    for e in palabras:
        if e not in tokens_ids:
            return False
        if tokens_ids[e] not in lista_ids_palabras:
            lista_ids_palabras.append(tokens_ids[e])

    lista_ids_resultantes = []
    if len(lista_ids_palabras) == 1:
        mostrar_tweets(lista_ids_palabras[0], tweets)
        return lista_ids_palabras[0]
    for id in lista_ids_palabras[0]:
        agregar = True
        for sub_id in lista_ids_palabras[1:]:
            if id not in sub_id:
                agregar = False
                break
        if agregar:
            lista_ids_resultantes.append(id)

    if lista_ids_resultantes == []:
        return False

    set_ids_resultantes = set(lista_ids_resultantes)

    mostrar_tweets(set_ids_resultantes, tweets)
    return set_ids_resultantes


# ---------------------------------------------------------------------------


def mostrar_tweets(ids, tweets):
    print(RESULTADOS_BUSQUEDA)
    for e in ids:
        print(f"{e}. {tweets[e]}")


# ---------------------------------------------------------------------------


def eliminar_tweet(tweets, tokens_ids):
    while True:
        tweets__encontrados = buscar_tweet(tweets, tokens_ids, "eliminar")
        if tweets__encontrados == "atras":
            break
        if not tweets__encontrados:
            break
        while True:
            ids = input("Ingrese los numeros de tweets a eliminar:\n")
            if verificar_ir_atras(ids):
                break
            lista_ids = ids.split(",")
            lista_ids_normalizada = normalizar_lista__ids(lista_ids)
            if not lista_ids_normalizada:
                print(INPUT_INVALIDO)
                continue
            set_ids = set(lista_ids_normalizada)
            tweets_eliminados = eliminar_tweet_e_ids_de_tokens(
                set_ids, tweets, tokens_ids
            )
            if not tweets_eliminados:
                print(NUMERO_INVALIDO)
                continue
            mostrar_tweets_eliminados(tweets_eliminados)
            break
        break


# ---------------------------------------------------------------------------


def normalizar_lista__ids(lista_ids):
    nueva_lista_ids = []

    for i in range(len(lista_ids)):
        if "-" in lista_ids[i] and lista_ids[i].count("-") == 1:
            rango = lista_ids[i].split("-")
            num1 = rango[0].strip()
            num2 = rango[1].strip()
            if num1 <= num2 and num1.isnumeric() and num2.isnumeric():
                for sub_i in range(int(num1), int(num2) + 1):
                    nueva_lista_ids.append(sub_i)
            else:
                return False
        elif not lista_ids[i].strip().isnumeric():
            return False
        else:
            nueva_lista_ids.append(int(lista_ids[i]))

    return nueva_lista_ids


# ---------------------------------------------------------------------------


def eliminar_tweet_e_ids_de_tokens(set_ids, tweets, tokens_ids):
    for e in set_ids:
        if e not in tweets:
            return False

    tweets_eliminados = {}

    for e in set_ids:
        tweet_normalizado = normalizar_texto(tweets[e])
        tweet_tokenizado_por_palabras = tweet_normalizado.split(" ")
        lista_tokens = tokenizar_por_segmentos(tweet_tokenizado_por_palabras)
        tweets_eliminados[e] = tweets[e]

        for token in lista_tokens:
            if len(tokens_ids[token]) > 1:
                tokens_ids[token].remove(e)
            else:
                tokens_ids.pop(token)

        tweets.pop(e)
    return tweets_eliminados


# ---------------------------------------------------------------------------


def mostrar_tweets_eliminados(tweets):
    print(TWEETS_ELIMINADOS_MENSAJE)
    for e in tweets:
        print(f"{e}. {tweets[e]}")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
