def count_list_item(list_content):
    float_list = []
    for item in list_content:
        float_list.append(float(item))
    print(float_list)

    result = sum(float_list)
    return result



a = ["1.3","2.4"]
print(count_list_item(a))