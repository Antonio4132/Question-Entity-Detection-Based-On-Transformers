# EE-BERT-T5

The EE-BERT-T5 experiment is based on the EE-SPECIE scheme, generalizing the obtaining of ontology entities. On executing the nextflow command, you have the following parameters:
1. entity: This parameter specifies the name of the folder in which the values are stored
of the entity and other files.
2. kv: kv or keyword, is the name of the ontology class from which to extract information.
3. model: specifies the model to use, the values are ”bert” or ”t5”.
4. finetune: this parameter can be activated with yes, in which case the program searches for a model
trained with model adaptation to use.

For instance:

```
nextflow run E1.nf –entity Specie –kw Specie –model bert –finetune yes
```
