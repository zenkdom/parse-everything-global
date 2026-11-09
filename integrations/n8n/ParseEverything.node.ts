import {
    IExecuteFunctions,
    INodeExecutionData,
    INodeType,
    INodeTypeDescription,
    NodeOperationError,
} from 'n8n-workflow';

export class ParseEverything implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'Parse Everything',
        name: 'parseEverything',
        icon: 'file:parseEverything.svg',
        group: ['transform'],
        version: 1,
        description: 'Bypass Cloudflare, Akamai and DataDome anti-bot protections',
        defaults: {
            name: 'Parse Everything',
        },
        inputs: ['main'],
        outputs: ['main'],
        credentials: [
            {
                name: 'parseEverythingApi',
                required: true,
            },
        ],
        properties: [
            {
                displayName: 'Target URL',
                name: 'targetUrl',
                type: 'string',
                default: '',
                placeholder: 'https://protected-site.com',
                required: true,
                description: 'The URL to scrape with anti-bot bypass',
            },
            {
                displayName: 'Render JavaScript',
                name: 'renderJs',
                type: 'boolean',
                default: false,
                description: 'Whether to execute dynamic JavaScript and wait for the DOM',
            },
            {
                displayName: 'Extract Clean Text Only',
                name: 'extractText',
                type: 'boolean',
                default: false,
                description: 'Whether to strip HTML tags and return pure text for LLMs',
            },
            {
                displayName: 'Country Code',
                name: 'countryCode',
                type: 'options',
                options: [
                    { name: 'United States (US)', value: 'US' },
                    { name: 'Germany (DE)', value: 'DE' },
                    { name: 'United Kingdom (GB)', value: 'GB' },
                ],
                default: 'US',
                description: 'Country for residential proxy routing',
            },
            {
                displayName: 'HTTP Method',
                name: 'method',
                type: 'options',
                options: [
                    { name: 'GET', value: 'GET' },
                    { name: 'POST', value: 'POST' },
                    { name: 'PUT', value: 'PUT' },
                ],
                default: 'GET',
                description: 'HTTP method to use when requesting the target URL',
            },
            {
                displayName: 'Request Body (JSON / Text)',
                name: 'body',
                type: 'string',
                default: '',
                description: 'Optional payload for POST/PUT requests',
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const returnData: INodeExecutionData[] = [];
        const credentials = await this.getCredentials('parseEverythingApi');
        const apiKey = credentials.apiKey as string;

        for (let i = 0; i < items.length; i++) {
            try {
                const targetUrl = this.getNodeParameter('targetUrl', i) as string;
                const renderJs = this.getNodeParameter('renderJs', i) as boolean;
                const extractText = this.getNodeParameter('extractText', i) as boolean;
                const countryCode = this.getNodeParameter('countryCode', i) as string;
                const method = (this.getNodeParameter('method', i, 'GET') as string) || 'GET';
                const bodyRaw = (this.getNodeParameter('body', i, '') as string) || '';

                let parsedBody: any = undefined;
                if (bodyRaw) {
                    try {
                        parsedBody = JSON.parse(bodyRaw);
                    } catch {
                        parsedBody = bodyRaw;
                    }
                }

                const response = await this.helpers.request({
                    method: 'POST',
                    url: 'https://parse-everything.com/api/v1/extract',
                    headers: {
                        Authorization: `Bearer ${apiKey}`,
                        'Content-Type': 'application/json',
                    },
                    body: {
                        target_url: targetUrl,
                        method,
                        body: parsedBody,
                        render_js: renderJs,
                        extract_text: extractText,
                        country_code: countryCode,
                        auto_detect: true,
                    },
                    json: true,
                });

                returnData.push({
                    json: response.data || response,
                });
            } catch (error) {
                if (this.continueOnFail()) {
                    returnData.push({ json: { error: (error as Error).message } });
                    continue;
                }
                throw new NodeOperationError(this.getNode(), error as Error);
            }
        }

        return [returnData];
    }
}
