def reordering_endpoints_paths(result: dict, **kwargs) -> dict:
    """
    Reorder OpenAPI endpoints: considering (most relevant paths in plural) first
    """

    # starts new dict order with plural endpoints first
    initial_paths = {}
    final_paths = {}
    for path_url, path_content in result['paths'].items():
        if path_url.startswith('/transactions'):
            initial_paths[path_url] = path_content
        else:
            final_paths[path_url] = path_content

    # add sorted paths in openapi response
    initial_paths.update(**final_paths)
    result['paths'] = initial_paths

    # return openapi paths
    return result
