| **1** | **Estrutura vs. Valor em `depositariaDaEmissao`** | Ignorar a chave `type`; comparar apenas o texto interno (string). |
| **2** | **String vazia (`""`) × `null`** | Sempre contar como **acerto** quando o template tem `""` e o agente retorna `null`, ou vice versa |
| **3** | **Campos totalmente ignorados**<br>(não contam nem como acerto nem como erro) | `distribuicao[].custodianteCnpj`  <br>`criteriosDeRemuneracao.configuracaoIndexador.percentualDoIndexador`<br>`criteriosDeRemuneracao.configuracaoIndexador.proRata`<br>`garantias[].descricaoAdicional` |
| **4** | **`garantias[].subtipo`** | Avaliar normalmente **exceto** quando o valor do template é `"REAL_DIREITOS_CREDITORIOS"` → nesse caso ignorar. |
| **5** | **Frequências de Juros / Amortização** | `criteriosDeRemuneracao.frequenciaDeJuros` e `...frequenciaDaAmortizacao`: qualquer valor extraído é considerado **correto** (template está `null`). |
| **6** | **Nomes abreviados vs. razão social completa** | Tratar como **corretos** quando referem-se à mesma entidade:<br>• `distribuicao[].investidor.nome`<br>• `distribuicao[].investidor.dadosBancarios.razaoSocial`<br>• `bancoLiquidanteEmissor.razaoSocial` |
| **7** | **Normalização de formatos** | • Comparar CNPJs sem pontuação.<br>• Datas com/sem “T00:00:00” ou sufixo “Z” são equivalentes. |
| **8** | **Campos extras do agente** | Chaves inexistentes no template (ex.: `id`, `isNew`, `contaDeposito`) são ignoradas. |
| **9** | **Outras coincidências aceitas** | `""` vs. string abreviada quando regra 6 se aplica.
