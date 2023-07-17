from sentence_transformers import SentenceTransformer, util
sentences1 = ['Automation, Open Source, Selenium, Sahi, Testing Tools, Web Application Testing']

sentences2 = ['Automation Testing, Manual Testing, Selenium Web Driver']

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1= model.encode(sentences1, convert_to_tensor=True)
embedding_2 = model.encode(sentences2, convert_to_tensor=True)

cosine_scores =util.cos_sim(embedding_1, embedding_2)
#Output the pairs with their score
print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[0], sentences2[0], cosine_scores[0][0]))
