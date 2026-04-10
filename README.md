# Dofus Music Reload


Ce logiciel n'est en aucun cas lié de loin ou de près à Ankama, voici un communiqué de leur part sur les logiciels tiers.
"Ne s'agissant pas d'un outil officiellement pris en charge par Ankama, nous vous rappelons que nous ne pouvons pas garantir
la sécurité du logiciel et que son utilisation peut comporter des risques. En cas d'éventuelles violations de données ou de logs,
le joueur sera tenu responsable.
Si le logiciel est modifié pour aller chercher des informations dans le client ou ailleurs, la peine sera maximal pour les comptes pris à utiliser le logiciel dans cet états.
Les musiques doivent être obtenu de manière légale et renommé dans les dossiers correspondant."

Le logiciel Dofus Music ne fait que scanner l'écran à l'aide de Tesseract pour trouver la zone dans laquelle vous vous trouvez.
En fonction de l'éclairage de la zone, cela peut prendre plus ou moins de temps,
et le changement peut se produire au changement de map au lieu de l'arrivée initiale dans la zone.

Pour détecter si vous êtes en combat, le script va chercher le bouton abandonné qui est en dessous du bouton Prêt & Passer votre tour.
Il est impératif qu'il soit visible à l'écran pendant votre combat, ne caché par cette interface avec autre chose.

Pour que le logiciel fonctionne au mieux, affichez la zone en "Grand", pour cela ouvrez les paramètres,
allez dans ACCESSIBILITÉ et réglez Textes > Taille de tous les textes sur Grand.

Si vous modifiez la zone de recherche, il est toujours préférable de rechercher à peine plus grand que le texte,
si vous coupez les lettres cela peut nuire au bon fonctionnement du logiciel.

Le logiciel essaiera toujours de lire la musique la plus appropriée à la situation, mais s'il ne trouve pas le fichier correspondant,
il jouera une autre version, toujours la plus appropriée.
En d'autres termes, si la version 1.29 de la zone n'existe pas ou n'est pas trouvée, il jouera la version 2.0 et vis versa.

Le logiciel, s'il est téléchargé via mon GitHub, ne présente a priori aucun risque pour vous et votre ordinateur,
mais faites attention si vous vous le procurez via un tiers inconnu. Comme dit plus haut par Ankama : 
En cas d'éventuelles violations de données ou de logs, seul le joueur sera tenu responsable.

Pour finir, je n'aie pas vocation à le faire évoluer ou à corriger des bugs après sa publication, c'était un one shot, si quelqu'un est assez débrouillard pour le faire fonctionner,
et le perfectionner, je suis heureux pour lui.

Je ne ferrai aucun SAV après publication.


Twitter : @SilamLiCrounch


###############################################################################
#  Il faut impérativement installer "tesseract-ocr-w64-setup-5.4.0.20240606"  #
#  avant de lancer Dofus Music.exe sinon la musique ne s'actualisera pas.     #
###############################################################################


\music

menu.wav

\music\3
musique_de_combat_aléatoire.wav (si la zone n'en a pas elle piochera une musique de combat ici.

\music\2
2nomdezone.wav
2nomdezonecombat.wav

\music\1
1nomdezone.wav
1nomdezonecombat.wav


Je liste les musiques tester et fonctionnelles avec leur nom :

\2
2abra.wav
2aerdala.wav
2akwadala.wav
2amakna.wav
2amaknacombat.wav
2ankmarecage.wav
2astrub.wav
2astrubcombat.wav
2bibli.wav
2bonta.wav
2bourgade.wav
2brakmar.wav
2brakmarcombat.wav
2bwork.wav
2cania.wav
2caniacombat.wav
2casjourfin.wav
2cavemine.wav
2chamakna.wav
2cimetière.wav
2cimetièrecombat.wav
2creperg.wav
2dedaldvcombat.wav
2dedaledv.wav
2dimobs.wav
2donjon.wav
2drag.wav
2ecaflipus.wav
2ecaflipuscombat.wav
2enutrosor.wav
2enutrosorcombat.wav
2fastrubkoala.wav
2fastrubkoalacombat.wav
2feudala.wav
2forpet.wav
2forpinperdu.wav
2frigost.wav
2frigostcombat.wav
2gelée.wav
2grobe.wav
2hakam.wav
2havresac.wav
2incarnam.wav
2ingloriom.wav
2jardhiv.wav
2karton.wav
2koalak.wav
2koalakcombat.wav
2larmeberceau.wav
2marecage.wav
2martegel.wav
2martegelcombat.wav
2mbcraque.wav
2mcraque.wav
2mino.wav
2minocombat.wav
2mkoalak.wav
2mkoalakcombat.wav
2moon.wav
2mooncombat.wav
2nowel.wav
2oreeenchant.wav
2oreeenchantcombat.wav
2osavora.wav
2osavoracombat.wav
2otomai.wav
2otomaicombat.wav
2pandala.wav
2pandalacombat.wav
2pastrub.wav
2pastrubcombat.wav
2plageamakna.wav
2plantala.wav
2porcos.wav
2portdegivre.wav
2rempvent.wav
2ruchglours.wav
2sidimote.wav
2sidimotecombat.wav
2srambad.wav
2srambadcombat.wav
2sufokia.wav
2sufokiacombat.wav
2taverne.wav
2tcra.wav
2tecaflip.wav
2teliotrop.wav
2teniripsa.wav
2tenutrof.wav
2terrdala.wav
2tfeca.wav
2thuppermage.wav
2tiop.wav
2tosamodas.wav
2touginak.wav
2tourboto.wav
2tourbotocombat.wav
2tourclep.wav
2tourclepcombat.wav
2tpandawa.wav
2trool.wav
2troublard.wav
2tsacrieur.wav
2tsadida.wav
2tsram.wav
2tsteamer.wav
2txelor.wav
2tzobal.wav
2vcanop.wav
2vpandalacombat.wav
2vulkania.wav
2vulkaniacombat.wav
2vzoth.wav
2wabbit.wav
2wabbitcombat.wav
2xelorium.wav
2xeloriumcombat.wav

\1
1amakna.wav
1amaknacombat.wav
1astrub.wav
1astrubcombat.wav
1bonta.wav
1bontacombat.wav
1brakmar.wav
1brakmarcombat.wav
1cania.wav
1cavemine.wav
1ccania.wav
1fastrubkoala.wav
1havresac.wav
1incarnam.wav
1koalak.wav
1mino.wav
1moon.wav
1nowel.wav
1otomai.wav
1otomaicombat.wav
1pandala.wav
1pastrub.wav
1sidimote.wav
1sidimotecombat.wav
1tcra.wav
1tecaflip.wav
1teniripsa.wav
1tenutrof.wav
1tfeca.wav
1tiop.wav
1tosamodas.wav
1trool.wav
1tsacrieur.wav
1tsadida.wav
1tsram.wav
1txelor.wav
1vkoalak.wav
1vpandala.wav
1wabbit.wav
