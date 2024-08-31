from flask import Flask, jsonify, request

app = Flask(__name__)

journals = [
    {'id': 1, 'title': 'Jornal-1', 'owner': 'mahela', 'entries': [
        {'id': 1, 'content': 'first part', 'date': '2024-08-29'},
        {'id': 2, 'content': 'second part', 'date': '2024-08-30'}
    ]},
]

def get_journal_by_id(journal_id):
    for journal in journals:
        if journal['id'] == journal_id:
            return journal
    return None

def get_entry_by_id(journal_id, entry_id):
    journal = get_journal_by_id(journal_id)
    if journal:
        for entry in journal['entries']:
            if entry['id'] == entry_id:
                return entry
    return None

# Journal endpoints
@app.route('/journals', methods=['GET'])
def get_journals():
    # Assuming authentication is in place to get the current user
    user_journals = [journal for journal in journals] 
    return jsonify({'journals': user_journals})

@app.route('/journals/<int:journal_id>', methods=['GET'])
def get_journal(journal_id):
    journal = get_journal_by_id(journal_id)
    if not journal:
        return jsonify({'error': 'Journal not found'}), 404
    return jsonify({'journal': journal})

@app.route('/journals', methods=['POST'])
def create_journal():
    journal = {
        'id': max(journal['id'] for journal in journals) + 1,
        'title': request.json['title'],
        'owner': request.json['owner'], 
        'entries': []
    }
    journals.append(journal)
    return jsonify({'journal': journal}), 201

@app.route('/journals/<int:journal_id>', methods=['PUT'])
def update_journal(journal_id):
    journal = get_journal_by_id(journal_id)
    if not journal:
        return jsonify({'error': 'Journal not found'}), 404
    journal['title'] = request.json.get('title', journal['title'])
    return jsonify({'journal': journal})

@app.route('/journals/<int:journal_id>', methods=['DELETE'])
def delete_journal(journal_id):
    journal = get_journal_by_id(journal_id)
    if not journal:
        return jsonify({'error': 'Journal not found'}), 404
    journals.remove(journal)
    return jsonify({'message': 'Journal deleted'})

# Journal Entry endpoints
@app.route('/journals/<int:journal_id>/entries', methods=['GET'])
def get_entries(journal_id):
    journal = get_journal_by_id(journal_id)
    if not journal:
        return jsonify({'error': 'Journal not found'}), 404
    return jsonify({'entries': journal['entries']})

@app.route('/journals/<int:journal_id>/entries', methods=['POST'])
def create_entry(journal_id):
    journal = get_journal_by_id(journal_id)
    if not journal:
        return jsonify({'error': 'Journal not found'}), 404
    entry = {
        'id': max(entry['id'] for entry in journal['entries']) + 1 if journal['entries'] else 1,
        'content': request.json['content'],
        'date': request.json['date']
    }
    journal['entries'].append(entry)
    return jsonify({'entry': entry}), 201

@app.route('/journals/<int:journal_id>/entries/<int:entry_id>', methods=['PUT'])
def update_entry(journal_id, entry_id):
    entry = get_entry_by_id(journal_id, entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    entry['content'] = request.json.get('content', entry['content'])
    entry['date'] = request.json.get('date', entry['date'])
    return jsonify({'entry': entry})

@app.route('/journals/<int:journal_id>/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(journal_id, entry_id):
    journal = get_journal_by_id(journal_id)
    if not journal:
        return jsonify({'error': 'Journal not found'}), 404
    entry = get_entry_by_id(journal_id, entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    journal['entries'].remove(entry)
    return jsonify({'message': 'Entry deleted'})

if __name__ == '__main__':
    app.run(debug=True)
