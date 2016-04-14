#!/usr/bin/env node

var rouge = require('rouge');
var fs = require('fs');

var candidate = fs.readFileSync(process.argv[2], 'utf8');
var reference = fs.readFileSync(process.argv[3], 'utf8');

var n = rouge.n(candidate, reference, 2);
console.log(n);
