# M1 - Data Preparation

## Data Source
**BEIR (Benchmarking Information Retrieval)** é uma biblioteca composta por vários datasets, cada um destinado a avaliar o desempenho de modelos de recuperação de informações em diferentes domínios, como por exemplo na saúde e tecnologia. Permitindo assim, que investigadores e desenvolvedores testem a eficácia dos modelos de pesquisa e recuperação em responder a consultas reais.

O **nfcorpus** é um desses datasets, disponibilizado pelo grupo [StatNLP](https://www.cl.uni-heidelberg.de/statnlpgroup/) - Statistical Natural Language Processing da Universidade de Heidelberg, focado especificamente no domínio nutricional.
Este contém pares de perguntas e documentos (respostas), onde os documentos contêm informações nutricionais e as perguntas representam possíveis consultas que os sistemas de recuperação devem responder. Por exemplo, uma pergunta pode ser "Qual é o teor de proteína no frango?", e o documento associado apresentará informações detalhadas sobre o frango, incluindo o teor de proteína.

Assim sendo, o **nfcorpus** foi desenvolvido para medir a capacidade de sistemas de recuperação de informações em encontrar respostas precisas e relevantes dentro de uma base de dados nutricional, servindo como uma ferramenta para benchmarking de sistemas de pesquisa.

## Licença
Este dataset é disponibilizador gratuitamente para fins académicos. No entanto, para qualquer outro uso é necessário consultar os Termos de Serviço do [NutritionFacts.org](https://nutritionfacts.org) e entrar em contacto direto com o autor dos dados, Sr. Michael Greger.


### Formato dos Dados
O dataset [BEIR/nfcorpus](https://ir-datasets.com/beir.html#beir/nfcorpus) é composto por três tipos de documentos distintos, organizados em três subconjuntos: treino, desenvolvimento e teste. Cada subconjunto contém:

- **Consultas do NutritionFacts.org** (.queries files): Documentos que contêm as perguntas ou consultas retiradas do site NutritionFacts.org, incluindo vídeos, blogs e Q&A. Estas consultas, são escritas em linguagem natural, sem uso de termos técnicos, facilitando a simulação de consultas reais de utilizadores.

- **Documentos Médicos** (.docs files): Documentos, na maioria extraídos do [Pubmed](https://pubmed.ncbi.nlm.nih.gov), que contêm os documentos médicos utilizados para responder às consultas. Estes são mais técnicos e detalhados, provenientes de fontes médicas e escritos em linguagem especializada.

- **Relevância de Pareamento** (.qrel files): Documentos que indicam a relevância de cada documento em relação às consultas, com diferentes níveis de relevância. A relevância é definida com base nas ligações entre os artigos do NutritionFacts.org e documentos médicos externos do PubMed:
  - **Nível mais relevante**: Documento com link direto num artigo do NutritionFacts.
  - **Segundo nível de relevância**: Documento citado por meio de um artigo intermediário do NutritionFacts.
  - **Menor nível de relevância**: Documento associado por meio de um sistema de tópicos/tags do NutritionFacts.

### Volume do Dataset
O dataset é dividido em três subconjuntos para treino, desenvolvimento e teste, distribuídos da seguinte forma:

- **80%** dos dados para treino,
- **10%** para desenvolvimento/validação,
- **10%** para teste.

Cada subconjunto é organizado no nível das consultas, ou seja, cada divisão inclui um conjunto diferente de consultas e documentos associados. A divisão permite avaliar modelos de recuperação em diferentes etapas: ajuste, validação e teste final.

Em vez de dividir os dados aleatoriamente, o BEIR/nfcorpus separa as consultas (ou perguntas) em cada conjunto. Isso significa que cada subconjunto contém um conjunto exclusivo de consultas e os documentos relevantes para responder a essas consultas. Essa organização é útil porque evita que as mesmas consultas apareçam em mais do que um conjunto, o que poderia enviesar os resultados ao fazer com que o modelo “treinasse” em consultas que ele veria novamente nos estágios de validação ou teste.

Para além disso, o BEIR/nfcorpus contém:

- **3.244 consultas** retiradas do site NutritionFacts.org. 
- **9.964 documentos médicos** provenientes, em sua maioria, da base de dados PubMed. 
- **169.756 julgamentos de relevância** que foram automaticamente atribuídos.

Esta estrutura e volume de dados permitem uma avaliação completa de modelos de recuperação de informações, garantindo que o modelo seja testado num número substancial de consultas e documentos, o que espelha as necessidades de informação no domínio médico.





