## Instructions for Information Extraction (Detailed Instructions)

## 1. Extraction Fields

### A. Parties (Partes)
Extract the following details:

- **Issuer (Emissor)**
- **Lead Coordinator (Coordenador Líder)**
- **Trustee Agent (Agente Fiduciário)**
- **Intervening Parties (Intervenientes)**
- **Registrar (Escriturador)**

### B. Characteristics (Características)
Extract the following details:

- **Emission Number (Número Emissão)**
- **Series (Série(s))**
- **Form (Forma)**
- **Type (Tipo)**
- **Species (Espécie)**
- **Emission Date (Data Emissão)**
- **Profitability Date (Data Rentabilidade)**
- **Maturity Date (Data Vencimento)**
- **Term (Prazo)**
- **Issuance Value (Valor da Emissão)**
- **Unit Value (Valor unitário)**
- **Issuance Quantity (Quantidade da Emissão)**
- **Use of Funds (Destinação dos Recursos)**
- **Emission Value Update (Atualização do valor da emissão)**
- **Profitability and Remuneration Data (Dados de Rentabilidade e Remuneração)**
- **Remuneration Payment (Pagamento da Remuneração)**
- **Amortization Payment (Pagamento da amortização)**
- **Extraordinary Amortization (Amortização Extraordinária)**
- **Optional Acquisition (Aquisição Facultativa)**
- **Early Redemption (Resgate Antecipado)**

### C. Guarantee and Early Maturity Data (Dados de Garantias e Vencimento Antecipado)
Extract the following details:

- **Issuer Obligations (Obrigações do Emissor)**
- **Early Maturities (Vencimentos Antecipados)**

---

## 2. General Extraction Rules

### **Monetary Formatting**
- All monetary values must adhere to the **Brazilian currency format** (e.g., `R$ 1.234.567,89`).
- If decimals are missing, append `,00`.

### **Missing Information**
- If a specific field is not found in the document, assign **"N/A"** as its value.

### **Completeness**
- The final **JSON output must include all the fields listed above**.
- No field should be omitted, even if the information is missing.
- No additional text or explanation should be present outside of this JSON object.

---

## 3. Chain-of-Thought (CoT) Reasoning

1. **Analyze the Document**  
   - Thoroughly read and analyze `main_document.md` to understand its content and locate relevant sections.

2. **Identify and Extract Information**  
   - Extract the data for each of the fields listed in **Sections A, B, and C**.

3. **Apply Formatting and Deduction Rules**  
   - Ensure monetary formatting is correct.
   - Replace missing values with `"N/A"`.

4. **Validate and Compile JSON**  
   - Ensure every field is accounted for.
   - Compile the extracted data into the final **JSON output**.

---

## 4. Expected JSON Schema

```json
{
  "Partes": {
    "Emissor": "string",
    "CoordenadorLider": "string",
    "AgenteFiduciario": "string",
    "Intervenientes": "string",
    "Escriturador": "string"
  },
  "Caracteristicas": {
    "NumeroEmissao": "string",
    "Series": "string",
    "Forma": "string",
    "Tipo": "string",
    "Especie": "string",
    "DataEmissao": "string",
    "DataRentabilidade": "string",
    "DataVencimento": "string",
    "Prazo": "string",
    "ValorDaEmissao": "string",
    "ValorUnitario": "string",
    "QuantidadeDaEmissao": "string",
    "DestinacaoDosRecursos": "string",
    "AtualizacaoValorEmissao": "string",
    "DadosRentabilidadeRemuneracao": "string",
    "PagamentoRemuneracao": "string",
    "PagamentoAmortizacao": "string",
    "AmortizacaoExtraordinaria": "string",
    "AquisicaoFacultativa": "string",
    "ResgateAntecipado": "string"
  },
  "GarantiasEVencimentosAntecipados": {
    "ObrigaçõesDoEmissor": "string",
    "VencimentosAntecipados": "string"
  }
}
```

