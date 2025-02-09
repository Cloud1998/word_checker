import json

def convert_to_element_plus_format(data):
    result = []
    for item in data:
        entry = {"value": item["code"], "label": item["name"]}  # 创建一个新的字典，包含 value 和 label 键
        if "children" in item:
            entry["children"] = convert_to_element_plus_format(item["children"])  # 递归处理子节点
        result.append(entry)
    return result


def main():
    # 假设你的 JSON 数据存储在文件 data.json 中
    with open('PCA-temp.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    element_plus_data = convert_to_element_plus_format(json_data)
    print(json.dumps(element_plus_data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()