let html = '';

process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => {
  html += chunk;
});

process.stdin.on('end', () => {
  const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!scriptMatch) {
    throw new Error('Script aplikasi tidak ditemukan pada response HTML.');
  }

  const elements = new Map();
  const document = {
    getElementById(id) {
      if (!elements.has(id)) {
        elements.set(id, {
          value: '',
          innerText: '',
          style: {},
          addEventListener() {},
        });
      }
      return elements.get(id);
    },
  };

  const manifest = [
    '- name: REDIS\\_PASSWORD',
    '  value: dummy-redis',
    '- name: AWS_ACCESS_KEY_ID',
    '  value: "dummy-access-key"',
    '- name: AWS_SECRET_ACCESS_KEY',
    '  value: "dummy-secret-key"',
  ].join('\n');

  const expectedKeys = [
    'REDIS_PASSWORD',
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
  ].join('\n');

  const expectedYaml = [
    '  - name: REDIS_PASSWORD',
    '    valueFrom:',
    '      secretKeyRef:',
    '        name: apps-data',
    '        key: REDIS_PASSWORD',
    '  - name: AWS_ACCESS_KEY_ID',
    '    valueFrom:',
    '      secretKeyRef:',
    '        name: apps-data',
    '        key: AWS_ACCESS_KEY_ID',
    '  - name: AWS_SECRET_ACCESS_KEY',
    '    valueFrom:',
    '      secretKeyRef:',
    '        name: apps-data',
    '        key: AWS_SECRET_ACCESS_KEY',
  ].join('\n');

  const expectedSecretYaml = [
    'kind: Secret',
    'apiVersion: v1',
    'metadata:',
    '  name: apps-data',
    '  namespace: testing',
    '  uid:',
    "  resourceVersion: '389295843'",
    "  creationTimestamp: '2026-09-05T17:26:12Z'",
    '  managedFields:',
    '    - manager: Mozilla',
    '      operation: Update',
    '      apiVersion: v1',
    "      time: '2026-09-05T17:35:01Z'",
    '      fieldsType: FieldsV1',
    '      fieldsV1:',
    "        'f:data':",
    '          .: {}',
    "          'f:REDIS_PASSWORD': {}",
    "          'f:AWS_ACCESS_KEY_ID': {}",
    "          'f:AWS_SECRET_ACCESS_KEY': {}",
    "        'f:type': {}",
    'data:',
    '  REDIS_PASSWORD: ZHVtbXktcmVkaXM=',
    '  AWS_ACCESS_KEY_ID: ZHVtbXktYWNjZXNzLWtleQ==',
    '  AWS_SECRET_ACCESS_KEY: ZHVtbXktc2VjcmV0LWtleQ==',
    'type: Opaque',
  ].join('\n');

  const expectedInjectSecretYaml = [
    'apiVersion: v1',
    'kind: Secret',
    'metadata:',
    '  name: apps-data',
    '  namespace:',
    'type: Opaque',
    'stringData:',
    '  REDIS_PASSWORD: "dummy-redis"',
    '  AWS_ACCESS_KEY_ID: "dummy-access-key"',
    '  AWS_SECRET_ACCESS_KEY: "dummy-secret-key"',
  ].join('\n');

  const assertions = `
    rawInput.value = manifest;
    namespaceInput.value = 'testing';
    processText();
    if (extractedKeys.value !== expectedKeys) {
      throw new Error('Extracted keys tidak sesuai: ' + extractedKeys.value);
    }
    if (yamlOutput.value !== expectedYaml) {
      throw new Error('Generated YAML tidak sesuai: ' + yamlOutput.value);
    }
    if (keyCount.innerText !== '3 keys') {
      throw new Error('Key count tidak sesuai: ' + keyCount.innerText);
    }
    if (secretYamlOutput.value !== expectedSecretYaml) {
      throw new Error('Secret YAML tidak sesuai: ' + secretYamlOutput.value);
    }
    if (injectSecretOutput.value !== expectedInjectSecretYaml) {
      throw new Error('Inject secret.yaml tidak sesuai: ' + injectSecretOutput.value);
    }

    rawInput.value = '- name: EMPTY_VALUE\\n  value:';
    namespaceInput.value = '';
    processText();
    const emptyDataLine = secretYamlOutput.value
      .split('\\n')
      .find(line => line.startsWith('  EMPTY_VALUE:'));
    if (emptyDataLine !== '  EMPTY_VALUE: ') {
      throw new Error('Value kosong masih memiliki tanda petik: ' + emptyDataLine);
    }
  `;

  new Function(
    'document',
    'manifest',
    'expectedKeys',
    'expectedYaml',
    'expectedSecretYaml',
    'expectedInjectSecretYaml',
    scriptMatch[1] + assertions,
  )(
    document,
    manifest,
    expectedKeys,
    expectedYaml,
    expectedSecretYaml,
    expectedInjectSecretYaml,
  );

  console.log('JavaScript parser smoke test: OK');
});
