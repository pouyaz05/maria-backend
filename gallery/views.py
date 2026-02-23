def painting_list_api(request):
    paintings = Painting.objects.all().order_by("-id")

    data = [{
        "id": p.id,
        "title": p.title,
        "artist_name": p.artist_name,
        "description": p.description,
        "year": p.year_created,
        "image": p.image.url if p.image else None,
    } for p in paintings]

    return JsonResponse(data, safe=False)