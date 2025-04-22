# CBR-2024

Códigos e materiais da programação para o desafio da categoria Challenge da CBR (Competição Brasileira de Robótica) 2024, da equipe RoboForge.

- **Rascunhos**: A pasta `/drafts` contém arquivos, materiais e códigos referentes a testes, rascunhos e algoritmos implementados em fase de validação.
- **Código Fonte**: o projeto a ser transferido e executado no robô está na pasta `/src`.
- **Regras**: as regras da competição estão descritas no documento `/regras.pdf`.
- **Documentação**: pasta `/docs`, e clicando [aqui](docs/README.md).

# Configurações do Projeto

## Extensão EV3

Para enviar apenas as pastas desejadas pro EV3, utilizamos as configurações da extensão do VSCode ev3dev-browser. O conteúdo é um padrão _glob_ incluindo a lista de _wildcards_ dos arquivos a serem incluidos no download pro brick.

No exemplo, enviando todos os arquivos da pasta `src` e da pasta `drafts`.

```json
{
  "ev3devBrowser.download.include": "{src/**,drafts/**}"
}
```

Para baixar as pastas direto na pasta root do EV3:

```json
{
  "ev3devBrowser.download.directory": "/"
}
```

# Comandos SSH

Pra baixar todos os logs do EV3 e deletar eles do robô:

```
scp robot@lilo:/home/robot/**/*.csv ./logs/ && ssh robot@lilo rm /home/robot/**/*.csv
```

Pra mudar o nome do robô:

```
sudo hostnamectl set-hostname stitch
```
