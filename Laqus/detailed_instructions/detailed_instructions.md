## Instructions for Information Extraction

Instructions for Information Extraction

Use the guidelines below to extract and structure every field from the document into a single JSON object that exactly matches the schema. Do not include any extra text—only return the JSON.

### Fields and Descriptions:

1. **emissorId**:

   * UUID of the issuer.
   * Type: `string`

2. **codigoExterno**:

   * External reference code for the issuance.
   * Type: `string`

3. **numeroEmissao**:

   * Sequential issuance number.
   * Type: `integer`

4. **numeroSerie**:

   * Series identifier.
   * Type: `string`

5. **tipoSerie**:

   * Series type (e.g., “SENIOR”).
   * Type: `string`

6. **regimeFiduciario**:

   * Whether the issuance is under fiduciary regime.
   * Type: `boolean`

7. **distribuicaoPublica**:

   * Whether it is a public distribution.
   * Type: `boolean`

8. **negociacaoSecundariaPor**:

   * Secondary trading designation (e.g., “INVESTIDOR\_PROFISSIONAL”).
   * Type: `string`

9. **cartulaEmissaoFormalizado**:

   * Whether the issuance certificate is formalized.
   * Type: `boolean`

10. **depositariaEmissao**:

    * Name of the depositary for the issuance.
    * Type: `string`

11. **utilizacaoAnuncioInicioDistribuicao**:

    * Whether an announcement starts distribution.
    * Type: `boolean`

12. **ufLocalEmissao**:

    * State code where issuance occurs.
    * Type: `string`

13. **localEmissao**:

    * Textual location of issuance.
    * Type: `string`

14. **classificadoraRisco1 / rating1**:

    * First risk classifier and its rating.
    * Type: `string`

15. **classificadoraRisco2 / rating2**:

    * Second risk classifier and its rating.
    * Type: `string`

16. **ufLocalPagamento**:

    * State code for payment location.
    * Type: `string`

17. **localPagamento**:

    * Textual payment location.
    * Type: `string`

18. **custodiantes (array)**:

* **cnpjInstituicaoCustodiante**: CNPJ of custodian institution.
* **razaoSocialInstituicaoCustodiante**: Legal name.
* **investidoresPrivados (array)**:

  * **cpfCnpj**: `string`
  * **razaoSocial**: `string`
  * **investidorId**: `string`
  * **quantidade**: `integer`
  * **ispbBanco**: `string`
  * **razaoSocialBanco**: `string`
  * **agenciaBanco**: `string`
  * **contaBanco**: `string`
* **informacoesBancarias (array)**:

  * **ispbBanco**: `string`
  * **razaoSocialBanco**: `string`
  * **agenciaBanco**: `string`
  * **contaBanco**: `string`

19. **utilizacaoFaculdadeParagrafo3Art7**:

    * Whether paragraph 3 of Art. 7 is applied.
    * Type: `boolean`

20. **nomeResponsavelPelasInformacoesDRI / emailResponsavelPelasInformacoesDRI**:

    * Contact person’s name and email for DRI information.
    * Type: `string`

21. **bancoLiquidanteEmissor / cnpjBancoLiquidanteEmissor**:

    * Name and CNPJ of liquidating bank.
    * Type: `string`

22. **codigoBancoContaCorrenteVinculadaEmissao / numeroAgenciaContaCorrenteVinculadaEmissao / numeroContaCorrenteVinculadaEmissao**:

    * Bank code, agency, and account for the linked current account.
    * Type: `string`

23. **tipoLiquidacao**:

    * Settlement type (e.g., “DIRETA”).
    * Type: `string`

24. **descricaoAdicional**:

    * Any additional description.
    * Type: `string`

25. **garantias (array)**:

* **id**: `integer`
* **subTipos (array)**:

  * **id**: `integer`

26. **descricaoAdicionalGarantias**:

    * Additional description for guarantees.
    * Type: `string`

27. **chaveExterna / isin**:

    * External key and ISIN code.
    * Type: `string`

28. **coobrigacao**:

    * Whether there is co-obligation.
    * Type: `boolean`

29. **naturezaAgenteFiduciario / razaoSocialAgenteFiduciario / cpfCnpjAgenteFiduciario**:

    * Nature, legal name, and CNPJ of the fiduciary agent.
    * Type: `string`

30. **tipoDistribuicaoPublica**:

    * Public distribution type.
    * Type: `string`

31. **coordenadoresIds (array of string)**:

    * IDs of coordinators.
    * Type: `string[]`

32. **coordenadorLiderId**:

    * Leader coordinator ID.
    * Type: `string`

33. **razaoSocialEscriturador / cnpjEscriturador / cnpjEmissor**:

    * Legal names and CNPJs of registrar and issuer.
    * Type: `string`

34. **criteriosRemuneracao (object)**:

* **valorNominalUnitarioEmissao**: `number`
* **quantidadeEmitida**: `number`
* **volumeEmissao**: `number`
* **moedaEmissao**: `string`
* **dataEmissao**: `string` (datetime)
* **dataVencimento**: `string` (datetime)
* **dataInicioRentabilidade**: `string` (datetime)
* **indexador**: `string`
* **taxaJurosFixoSpread**: `number`
* **convencaoJurosFixos**: `string`
* **custoEmissao (object)**:

  * **custoTotal**: `number`
  * **feeLaqusBruto**: `number`

35. **amortizacaoSobre**:

    * “PRINCIPAL” or other.
    * Type: `string`

36. **amortizacaoPassivelAoTermoSecuritizacao**:

    * Whether amortization applies at the securitization term.
    * Type: `boolean`

37. **amortizacoes (array)**:

* **percentualAmortizacao**: `number`
* **dataAmortizacao**: `string` (ISO datetime)
* **isNew**: `boolean`
* **id**: `string`

38. **pagamentoJuros / incorporacaoJuros (objects)**:

* **datas**: array of date strings (`"YYYY-MM-DD HH:MM:SS"`)

39. **possuiResgateAntecipado**:

    * Whether early redemption is available.
    * Type: `boolean`

40. **documents (array of objects)**:

    * Embedded document references.
    * Type: `object[]`



### Specific Rules:

1. **Monetary Formatting**:

   - All monetary values must use the **Brazilian format**: `R$ 1.234.567,89`.
   - Add `,00` if decimals are missing in the document.

2. **Missing Information**:
  - If a field is not found, return:
      - `"N/A"` for each field that falls into this condition of not being found in the document, a value.

3. **Output Completeness:**:

   - You must return all requested fields and items as a complete JSON object.
   - Under no circumstances should you omit any items or fields, even partially. If the total output exceeds the token limit, split the response into multiple JSON objects, each containing sequential parts of the data, clearly labeled.

4. **Output Consistency**:

   - Ensure the JSON output strictly matches the schema provided, with no missing fields or deviations.

5. **Item limitation**:
   - The number of items in the "Itens" array can vary, However, in some cases there will be several items contained in a single document, which can overload the response and return missing information, so it must be limited to just 30 items, if the document exceeds this limit, just ignore the rest, return only the first 30 items.


### Schema of Expected Output:


```json
{
  "type": "object",
  "properties": {
    "emissorId": { "type": "string" },
    "codigoExterno": { "type": "string" },
    "numeroEmissao": { "type": "integer" },
    "numeroSerie": { "type": "string" },
    "tipoSerie": { "type": "string" },
    "regimeFiduciario": { "type": "boolean" },
    "distribuicaoPublica": { "type": "boolean" },
    "negociacaoSecundariaPor": { "type": "string" },
    "cartulaEmissaoFormalizado": { "type": "boolean" },
    "depositariaEmissao": { "type": "string" },
    "utilizacaoAnuncioInicioDistribuicao": { "type": "boolean" },
    "ufLocalEmissao": { "type": "string" },
    "localEmissao": { "type": "string" },
    "classificadoraRisco1": { "type": "string" },
    "rating1": { "type": "string" },
    "classificadoraRisco2": { "type": "string" },
    "rating2": { "type": "string" },
    "ufLocalPagamento": { "type": "string" },
    "localPagamento": { "type": "string" },
    "custodiantes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "cnpjInstituicaoCustodiante": { "type": "string" },
          "razaoSocialInstituicaoCustodiante": { "type": "string" },
          "investidoresPrivados": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "cpfCnpj": { "type": "string" },
                "razaoSocial": { "type": "string" },
                "investidorId": { "type": "string" },
                "quantidade": { "type": "integer" },
                "ispbBanco": { "type": "string" },
                "razaoSocialBanco": { "type": "string" },
                "agenciaBanco": { "type": "string" },
                "contaBanco": { "type": "string" }
              }
            }
          },
          "informacoesBancarias": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ispbBanco": { "type": "string" },
                "razaoSocialBanco": { "type": "string" },
                "agenciaBanco": { "type": "string" },
                "contaBanco": { "type": "string" }
              }
            }
          }
        }
      }
    },
    "utilizacaoFaculdadeParagrafo3Art7": { "type": "boolean" },
    "nomeResponsavelPelasInformacoesDRI": { "type": "string" },
    "emailResponsavelPelasInformacoesDRI": { "type": "string" },
    "bancoLiquidanteEmissor": { "type": "string" },
    "cnpjBancoLiquidanteEmissor": { "type": "string" },
    "codigoBancoContaCorrenteVinculadaEmissao": { "type": "string" },
    "numeroAgenciaContaCorrenteVinculadaEmissao": { "type": "string" },
    "numeroContaCorrenteVinculadaEmissao": { "type": "string" },
    "tipoLiquidacao": { "type": "string" },
    "descricaoAdicional": { "type": "string" },
    "garantias": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "integer" },
          "subTipos": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": { "type": "integer" }
              }
            }
          }
        }
      }
    },
    "descricaoAdicionalGarantias": { "type": "string" },
    "chaveExterna": { "type": "string" },
    "isin": { "type": "string" },
    "coobrigacao": { "type": "boolean" },
    "naturezaAgenteFiduciario": { "type": "string" },
    "razaoSocialAgenteFiduciario": { "type": "string" },
    "cpfCnpjAgenteFiduciario": { "type": "string" },
    "tipoDistribuicaoPublica": { "type": "string" },
    "coordenadoresIds": {
      "type": "array",
      "items": { "type": "string" }
    },
    "coordenadorLiderId": { "type": "string" },
    "razaoSocialEscriturador": { "type": "string" },
    "cnpjEscriturador": { "type": "string" },
    "cnpjEmissor": { "type": "string" },
    "criteriosRemuneracao": {
      "type": "object",
      "properties": {
        "valorNominalUnitarioEmissao": { "type": "number" },
        "quantidadeEmitida": { "type": "number" },
        "volumeEmissao": { "type": "number" },
        "moedaEmissao": { "type": "string" },
        "dataEmissao": { "type": "string" },
        "dataVencimento": { "type": "string" },
        "dataInicioRentabilidade": { "type": "string" },
        "indexador": { "type": "string" },
        "taxaJurosFixoSpread": { "type": "number" },
        "convencaoJurosFixos": { "type": "string" },
        "custoEmissao": {
          "type": "object",
          "properties": {
            "custoTotal": { "type": "number" },
            "feeLaqusBruto": { "type": "number" }
          }
        }
      }
    },
    "amortizacaoSobre": { "type": "string" },
    "amortizacaoPassivelAoTermoSecuritizacao": { "type": "boolean" },
    "amortizacoes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "percentualAmortizacao": { "type": "number" },
          "dataAmortizacao": { "type": "string" },
          "isNew": { "type": "boolean" },
          "id": { "type": "string" }
        }
      }
    },
    "pagamentoJuros": {
      "type": "object",
      "properties": {
        "datas": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "incorporacaoJuros": {
      "type": "object",
      "properties": {
        "datas": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "possuiResgateAntecipado": { "type": "boolean" },
    "documents": {
      "type": "array",
      "items": { "type": "object" }
    }
  }
}
```