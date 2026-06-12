def build_label_maps(labels):
    unique_labels = sorted(set(labels))
    label_to_id = {label: i for i, label in enumerate(unique_labels)}
    id_to_label = {i: label for label, i in label_to_id.items()}
    return label_to_id, id_to_label

def encode_labels(labels, label_to_id):
    return [label_to_id[label] for label in labels]