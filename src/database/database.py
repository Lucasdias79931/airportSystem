import os
import pickle

class DiskBTreeNode:
    def __init__(self, node_id, t, leaf=True):
        self.node_id = node_id
        self.t = t
        self.leaf = leaf
        self.keys : list[str]= []
        self.values = []
        self.children = []   

class DiskBTree:
    root_id : int = 0; 

    def __init__(self, path, t=3):
        self.directory = path
        self.t = t

        os.makedirs(path, exist_ok=True)

        meta_file = os.path.join(path, "meta.pkl")

        if os.path.exists(meta_file):
            self._load_meta()
        else:
            self.next_id = 1
            self.root_id = self._create_node(leaf=True).node_id;
            self._save_meta()

    def _node_file(self, node_id):
        return os.path.join(self.directory, f"node_{node_id}.pkl")

    def _save_node(self, node):
        data = {
            "leaf": node.leaf,
            "keys": node.keys,
            "values": node.values,
            "children": node.children,
            "t": node.t
        }
        with open(self._node_file(node.node_id), "wb") as f:
            pickle.dump(data, f)

    def _load_node(self, node_id) -> DiskBTreeNode:
        with open(self._node_file(node_id), "rb") as f:
            data = pickle.load(f)

        node = DiskBTreeNode(
            node_id=node_id,
            t=data["t"],
            leaf=data["leaf"]
        )
        node.keys = data["keys"]
        node.values = data["values"]
        node.children = data["children"]
        return node

    def _create_node(self, leaf) -> DiskBTreeNode:
        node = DiskBTreeNode(self.next_id, self.t, leaf)
        self._save_node(node);
        self.next_id += 1;
        self._save_meta();
        return node;

    def _save_meta(self):
        meta = {
            "root_id": self.root_id,
            "next_id": self.next_id,
            "t": self.t
        }
        with open(os.path.join(self.directory, "meta.pkl"), "wb") as f:
            pickle.dump(meta, f)

    def _load_meta(self) -> None:
        with open(os.path.join(self.directory, "meta.pkl"), "rb") as f:
            meta = pickle.load(f)

        self.root_id = meta["root_id"]
        self.next_id = meta["next_id"]
        self.t = meta["t"]

    def search(self, cpf : str, node_id=None):
        if node_id is None:
            node_id = self.root_id

        node = self._load_node(node_id)

        i = 0
        while i < len(node.keys) and cpf > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == cpf:
            return node.values[i]

        if node.leaf:
            return None

        return self.search(cpf, node.children[i])

    def insert(self, key : str, value):
        root = self._load_node(self.root_id)
        if len(root.keys) == 2 * self.t - 1:
            new_root = self._create_node(leaf=False)
            new_root.children.append(self.root_id)
            self._split_child(new_root, 0)
            self.root_id = new_root.node_id
            self._save_meta()
            self._insert_non_full(new_root, key, value)
            self._save_node(new_root)
        else:
            self._insert_non_full(root, key, value)
            self._save_node(root)

    def _insert_non_full(self, node, key : str, value):
        i = len(node.keys) - 1

        #assert type(key) == "str";

        if node.leaf:
            node.keys.append(None)
            node.values.append(None)

            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1

            node.keys[i+1] = key
            node.values[i+1] = value
            self._save_node(node)

        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            child = self._load_node(node.children[i])

            if len(child.keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
                child = self._load_node(node.children[i])

            self._insert_non_full(child, key, value)

    def _split_child(self, parent, index):
        t = self.t
        full = self._load_node(parent.children[index])

        new = self._create_node(leaf=full.leaf)

        parent.keys.insert(index, full.keys[t-1])
        parent.values.insert(index, full.values[t-1])
        parent.children.insert(index + 1, new.node_id)

        new.keys = full.keys[t:]
        new.values = full.values[t:]

        full.keys = full.keys[:t-1]
        full.values = full.values[:t-1]

        if not full.leaf:
            new.children = full.children[t:]
            full.children = full.children[:t]

        self._save_node(full)
        self._save_node(new)
        self._save_node(parent)

    def update(self, key : str, new_value) -> bool:
        return self._update_recursive(key, new_value, self.root_id);


    def _update_recursive(self, key : str, new_value, node_id: int) -> bool:
        node = self._load_node(node_id)

        # 1. Find the first key >= target key
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # 2. Key found in this node → update
        if i < len(node.keys) and node.keys[i] == key:
            node.values[i] = new_value
            self._save_node(node)
            return True

        # 3. If leaf → key doesn't exist
        if node.leaf:
            return False

        # 4. Recurse into the correct child
        return self._update_recursive(key, new_value, node.children[i])


    def getAll(self) -> list:
        """Return a list of all values in the B-Tree."""
        result = []
        self._collect(self.root_id, result)
        return result

    def _collect(self, node_id: int, out_list: list):
        """Recursive in-order traversal collecting all values."""
        node = self._load_node(node_id)

        if node.leaf:
            # Leaf: just append all values
            out_list.extend(node.values)
        else:
            # Internal node:
            # traverse child, then key/value, child, key/value, ...
            for i in range(len(node.keys)):
                self._collect(node.children[i], out_list)
                out_list.append(node.values[i])
            # final child
            self._collect(node.children[-1], out_list)

    def getByName(self, name: str) -> list:
        result = []
        self._collect_by_name(self.root_id, name, result)
        return result

    def _collect_by_name(self, node_id: int, name: str, out_list: list):
        node = self._load_node(node_id)

        if node.leaf:
            for v in node.values:
                if v.name == name:
                    out_list.append(v)
        else:
            for i in range(len(node.keys)):
                self._collect_by_name(node.children[i], name, out_list)
                if node.values[i].name == name:
                    out_list.append(node.values[i])
            self._collect_by_name(node.children[-1], name, out_list)

