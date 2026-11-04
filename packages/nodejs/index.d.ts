export interface ScrapeOptions {
    target_url?: string;
    url?: string;
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | string;
    body?: any;
    post_data?: any;
    render_js?: boolean;
    auto_detect?: boolean;
    bypass_cloudflare?: boolean;
    bypass_akamai?: boolean;
    country_code?: string;
    extract_text?: boolean;
    selectors?: Record<string, string>;
    wait_for_selector?: string;
    custom_headers?: Record<string, string>;
    cookies?: Record<string, string>;
    timeout?: number;
    session_id?: string;
}

export interface ScrapeResponseData {
    http_status: number;
    page_title?: string;
    content_length: number;
    execution_time_seconds: number;
    protection_bypassed: string;
    full_html?: string;
    clean_text?: string;
    selectors_data?: Record<string, string[]>;
}

export interface ScrapeResponse {
    status: string;
    timestamp: string;
    engine_used: string;
    credits_charged: number;
    data: ScrapeResponseData;
}

export interface BatchResponse {
    status: string;
    batch_id: string;
    total_urls: number;
    message: string;
}

export interface BatchStatusResponse {
    status: string;
    batch_id: string;
    job_status: 'pending' | 'in_progress' | 'completed' | 'failed';
    total_urls: number;
    completed_urls: number;
    progress_percent: number;
    items: Array<{
        target_url: string;
        status: string;
        http_status: number;
        execution_time: number;
        result_json?: string;
    }>;
}

export class ParseEverythingError extends Error {
    statusCode?: number;
    responseBody?: string;
}

export class ParseEverything {
    constructor(apiKey: string, options?: { baseUrl?: string });
    scrape(params: ScrapeOptions): Promise<ScrapeResponse>;
    get(targetUrl: string, options?: Partial<ScrapeOptions>): Promise<ScrapeResponse>;
    post(targetUrl: string, body?: any, options?: Partial<ScrapeOptions>): Promise<ScrapeResponse>;
    batch(targetUrls: string[], options?: { render_js?: boolean; country_code?: string; webhook_url?: string }): Promise<BatchResponse>;
    getBatch(batchId: string): Promise<BatchStatusResponse>;
}
