import os
import tempfile
from io import StringIO, RawIOBase

import bson as bson
import happybase
from flask import Flask, request
from warcio import WARCWriter, StatusAndHeaders

app = Flask(__name__)
connection = happybase.Connection()
table = connection.table('main')


class BytesIOWrapper(RawIOBase):
    def __init__(self, file, encoding='utf-8', errors='strict'):
        self.file, self.encoding, self.errors = file, encoding, errors
        self.buf = b''

    def readinto(self, buf):
        if not self.buf:
            self.buf = self.file.read(4096).encode(self.encoding, self.errors)
            if not self.buf:
                return 0
        length = min(len(buf), len(self.buf))
        buf[:length] = self.buf[:length]
        self.buf = self.buf[length:]
        return length

    def readable(self):
        return True


@app.route('/', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json

        new_file, path = tempfile.mkstemp()
        with open(path, 'wb') as f:
            writer = WARCWriter(f, gzip=True)
            for uuid in json:
                row = table.row(uuid)
                if b'cf1:IF' not in row:
                    record = writer.create_warc_record(uuid, 'metadata',
                                                       payload=BytesIOWrapper(StringIO("Entry does not found.")))
                else:
                    inter_format = bson.loads(row[b'cf1:IF'])
                    http_headers = StatusAndHeaders('200 OK', [], protocol='HTTP/1.0')
                    record = writer.create_warc_record(inter_format['url'], 'response',
                                                       payload=BytesIOWrapper(StringIO(str(row[b'cf1:plain-text']))),
                                                       http_headers=http_headers,
                                                       warc_headers_dict=inter_format['rec-headers'],
                                                       warc_content_type=inter_format['rec-headers']['Content-Type'])
                writer.write_record(record)

        def generate():
            try:
                with open(path, 'rb') as fr:
                    yield from fr
            finally:
                os.remove(path)

        r = app.response_class(generate(), mimetype='application/warc')
        r.headers.set('Content-Disposition', 'attachment', filename='export.warc.gz')
        return r
    else:
        return 'Content-Type not supported!'


if __name__ == '__main__':
    app.run()
