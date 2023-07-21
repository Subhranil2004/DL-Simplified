# -*- coding: utf-8 -*-
"""Market Basket Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZZhHNM1SPbjL7o3FZ7XJPihM5yhNnQz0
"""

import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

path = '/content/drive/My Drive/Colab Notebooks/Datasets/basket_analysis.csv'

df = pd.read_csv(path)

df = pd.DataFrame(df)

df.head()

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.frequent_patterns import association_rules

"""Preprocessing the data"""

# removing column 0 as it's unnecessary
df = df.drop(columns=['Unnamed: 0'])
transactions = df.apply(lambda row: df.columns[row.values], axis=1).tolist()

df.head()

"""Applying apriori algorithm"""

te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
frequent_itemsets_apriori = apriori(df_encoded, min_support=0.1, use_colnames=True)

"""Generating association rules for apriori"""

association_rules_apriori = association_rules(frequent_itemsets_apriori, metric='confidence', min_threshold=0.5)

print("Association Rules (Apriori):")
print(association_rules_apriori)

"""FP growth algorithm"""

frequent_itemsets_fpgrowth = fpgrowth(df_encoded, min_support=0.1, use_colnames=True)

"""Association rules for FP growth"""

association_rules_fpgrowth = association_rules(frequent_itemsets_fpgrowth, metric='confidence', min_threshold=0.5)

print("Association Rules (FP-Growth):")
print(association_rules_fpgrowth)

"""Comparing performance and results"""

apriori_freq_itemsets_count = frequent_itemsets_apriori.shape[0]
fpgrowth_freq_itemsets_count = frequent_itemsets_fpgrowth.shape[0]

"""Comparing no. of associations"""

apriori_association_rules_count = association_rules_apriori.shape[0]
fpgrowth_association_rules_count = association_rules_fpgrowth.shape[0]

"""Compare average antecedent and consequent lengths"""

apriori_avg_antecedent_len = association_rules_apriori.antecedents.apply(lambda x: len(x)).mean()
apriori_avg_consequent_len = association_rules_apriori.consequents.apply(lambda x: len(x)).mean()
fpgrowth_avg_antecedent_len = association_rules_fpgrowth.antecedents.apply(lambda x: len(x)).mean()
fpgrowth_avg_consequent_len = association_rules_fpgrowth.consequents.apply(lambda x: len(x)).mean()

"""Comparison Results"""

print("Comparison Results:")
print("-" * 50)
print("Frequent Itemsets Count:")
print("Apriori: ", apriori_freq_itemsets_count)
print("FP-Growth: ", fpgrowth_freq_itemsets_count)
print("-" * 50)
print("Number of Association Rules:")
print("Apriori: ", apriori_association_rules_count)
print("FP-Growth: ", fpgrowth_association_rules_count)
print("-" * 50)
print("Average Antecedent Length:")
print("Apriori: ", apriori_avg_antecedent_len)
print("FP-Growth: ", fpgrowth_avg_antecedent_len)
print("-" * 50)
print("Average Consequent Length:")
print("Apriori: ", apriori_avg_consequent_len)
print("FP-Growth: ", fpgrowth_avg_consequent_len)
print("-" * 50)

comparison_df = pd.DataFrame({
    'Algorithm': ['Apriori', 'FP-Growth'],
    'Frequent Itemsets Count': [apriori_freq_itemsets_count, fpgrowth_freq_itemsets_count],
    'Association Rules Count': [apriori_association_rules_count, fpgrowth_association_rules_count],
    'Average Antecedent Length': [apriori_avg_antecedent_len, fpgrowth_avg_antecedent_len],
    'Average Consequent Length': [apriori_avg_consequent_len, fpgrowth_avg_consequent_len]
})

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(data=comparison_df, x='Algorithm', y='Frequent Itemsets Count')
plt.title('Comparison of Frequent Itemsets Count')
plt.show()

"""### Conclusions based on the above dataset:

1. **Frequent itemsets count**: The FP-Growth algorithm outperforms the Apriori algorithm in terms of generating frequent itemsets. It produces a smaller number of frequent itemsets, indicating better efficiency and scalability.

2. **No. of Association rules**: The Apriori algorithm generates a higher number of association rules compared to the FP-Growth algorithm. This suggests that the Apriori algorithm explores more potential associations between items in the dataset.

3. **Avg. antecedent and consequent length**: The Apriori algorithm tends to produce association rules with longer antecedents and consequents compared to the FP-Growth algorithm.
---
* If efficiency and scalability are crucial, and a smaller number of frequent itemsets is sufficient for analysis, the FP-Growth algorithm is a better choice.
* If generating a larger number of association rules and exploring more detailed patterns is a priority, the Apriori algorithm can be preferred.
* The choice of algorithm should be based on the specific requirements and constraints of the analysis, such as dataset size, computational resources, and the desired level of granularity in the association rules.

**Result Interpretation:**


---


**Apriori Algorithm Results**:
* Bread --> Yogurt: Customers who purchase Bread are also likely to purchase Yogurt with a confidence of 50.26%.
* Ice cream --> Butter: Customers who purchase Ice cream are also likely to purchase Butter with a confidence of 50.49%.
* Dill --> Chocolate: Customers who purchase Dill are also likely to purchase Chocolate with a confidence of 50%.
* Milk --> Chocolate: Customers who purchase Milk are also likely to purchase Chocolate with a confidence of 52.1%.
* Chocolate --> Milk: Customers who purchase Chocolate are also likely to purchase Milk with a confidence of 50.12%.



---

**FP-Growth Algorithm Results**:
* Ice cream, Butter --> Chocolate: Customers who purchase Ice cream and Butter are also likely to purchase Chocolate with a confidence of 52.66%.
* Ice cream, Chocolate --> Butter: Customers who purchase Ice cream and Chocolate are also likely to purchase Butter with a confidence of 53.96%.
* Butter, Chocolate --> Ice cream: Customers who purchase Butter and Chocolate are also likely to purchase Ice cream with a confidence of 53.96%.
* Ice cream, Butter --> Sugar: Customers who purchase Ice cream and Butter are also likely to purchase Sugar with a confidence of 51.21%.
* Dill, Unicorn --> Chocolate: Customers who purchase Dill and Unicorn are also likely to purchase Chocolate with a confidence of 60.12%.
"""